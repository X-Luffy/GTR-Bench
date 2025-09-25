"""
GTR-Bench 评分系统
与app.py中的得分设计保持一致
"""

import re
from typing import Dict, List, Tuple
import numpy as np

class ScoringSystem:
    """评分系统类，负责计算答题得分和时间IoU"""
    
    def __init__(self):
        self.time_threshold = 300  # 5分钟时间阈值（秒）
    
    def calculate_score_new(self, case: Dict, user_answers: Dict, elapsed_time: float) -> Dict:
        """
        根据新要求计算答题得分
        
        Args:
            case: 题目案例数据
            user_answers: 用户答案
            elapsed_time: 答题时间（秒）
            
        Returns:
            得分结果字典
        """
        # 提取任务类型
        task_id = case.get('task_id', '')
        if task_id:
            task_type = task_id
        else:
            task_type = ''
        
        # 检查选项答案
        option_correct = self.check_option_answers(case, user_answers)
        
        # 根据任务类型计算得分
        if task_type in ["GeoLocation", "ArrivalTimeInterval", "MotionState", "CausalReordering"]:
            # 选择题任务：选择正确得1分，错误得0分
            score = 1.0 if option_correct else 0.0
            accuracy_score = score
            time_score = 0.0
            
        elif task_type in ["NextSpotForecasting", "MultiTargetTrajectoryForecasting"]:
            # 选择题+时间范围任务：选择正确才计算TimeIoU
            if option_correct:
                time_iou = self.calculate_time_range_iou(case, user_answers)
                score = time_iou
                accuracy_score = 1.0 if option_correct else 0.0
                time_score = time_iou
            else:
                score = 0.0
                accuracy_score = 0.0
                time_score = 0.0
                
        elif task_type == "TrajectoryForecasting":
            # 轨迹预测任务：独立计算两段得分并求平均
            # 首先从options数组中提取摄像头名称
            options = user_answers.get('options', [])
            if len(options) >= 2:
                # 将数组格式的答案转换为first_camera和second_camera格式
                user_answers['first_camera'] = options[0]
                user_answers['second_camera'] = options[1]
            
            # 映射时间范围字段
            if 'time_range_0_start' in user_answers and 'time_range_0_end' in user_answers:
                user_answers['first_start_time'] = user_answers['time_range_0_start']
                user_answers['first_end_time'] = user_answers['time_range_0_end']
            if 'time_range_1_start' in user_answers and 'time_range_1_end' in user_answers:
                user_answers['second_start_time'] = user_answers['time_range_1_start']
                user_answers['second_end_time'] = user_answers['time_range_1_end']
            
            first_score = self.calculate_trajectory_segment_score(case, user_answers, 'first')
            second_score = self.calculate_trajectory_segment_score(case, user_answers, 'second')
            score = (first_score + second_score) / 2.0
            
            # Calculate accuracy：两个摄像头都选择正确才算正确
            first_camera_correct = self.check_trajectory_camera_selection(case, user_answers, 'first')
            second_camera_correct = self.check_trajectory_camera_selection(case, user_answers, 'second')
            accuracy_score = 1.0 if (first_camera_correct and second_camera_correct) else 0.0
            time_score = score
        else:
            # 默认情况
            score = 1.0 if option_correct else 0.0
            accuracy_score = score
            time_score = 0.0
        
        return {
            'score': score,
            'MCQacc': accuracy_score,
            'TimeIoU': time_score,
            'elapsed_time': elapsed_time,
            'is_correct': option_correct,
            'task_type': task_type
        }
    
    def check_option_answers(self, case: Dict, user_answers: Dict) -> bool:
        """检查选项答案是否正确"""
        # 获取选项列表
        choices = case.get('choices', [])
        
        # 首先尝试从correct_cam_name字段获取正确答案
        correct_cam_names = case.get('correct_cam_name', [])
        if correct_cam_names:
            # 提取正确答案的选项字母
            gt_option = self.extract_option_letter(correct_cam_names[0], choices)
        else:
            # 如果没有correct_cam_name，尝试ground_truth字段
            ground_truth = case.get('ground_truth', {})
            if isinstance(ground_truth, dict) and 'correct_cam_name' in ground_truth:
                gt_option = self.extract_option_letter(ground_truth['correct_cam_name'][0], choices)
            else:
                gt_option = self.extract_option_letter(str(ground_truth), choices)
        
        user_options = user_answers.get('options', [])
        
        if not gt_option or not user_options:
            return False
        
        # 检查用户答案
        user_option_letters = []
        for option in user_options:
            letter = self.extract_option_letter(option, choices)
            if letter:
                user_option_letters.append(letter)
        
        # 判断是否正确
        return gt_option in user_option_letters
    
    def calculate_time_range_iou(self, case: Dict, user_answers: Dict) -> float:
        """计算时间范围IoU"""
        time_ious = []
        
        # 检查correct_time_str字段
        if 'correct_time_str' in case and case['correct_time_str']:
            for i, gt_time_str in enumerate(case['correct_time_str']):
                if '-' in gt_time_str:
                    # 时间范围格式
                    user_start_time = user_answers.get(f'time_range_{i}_start', '')
                    user_end_time = user_answers.get(f'time_range_{i}_end', '')
                    
                    if user_start_time and user_end_time:
                        iou = self.calculate_time_range_iou_single(gt_time_str, f"{user_start_time}-{user_end_time}")
                        time_ious.append(iou)
                else:
                    # 单个时间点
                    user_time = user_answers.get(f'time_range_{i}', '')
                    if user_time:
                        iou = self.calculate_time_iou(gt_time_str, user_time)
                        time_ious.append(iou)
        
        if not time_ious:
            return 0.0
        
        return np.mean(time_ious)
    
    def calculate_time_range_iou_single(self, gt_time_range: str, user_time_range: str) -> float:
        """计算单个时间范围的IoU"""
        try:
            # 解析真实时间范围
            gt_start, gt_end = gt_time_range.split('-')
            gt_start_seconds = self.time_to_seconds(gt_start)
            gt_end_seconds = self.time_to_seconds(gt_end)
            
            # 解析用户时间范围
            user_start, user_end = user_time_range.split('-')
            user_start_seconds = self.time_to_seconds(user_start)
            user_end_seconds = self.time_to_seconds(user_end)
            
            # 计算交集
            intersection_start = max(gt_start_seconds, user_start_seconds)
            intersection_end = min(gt_end_seconds, user_end_seconds)
            
            if intersection_end <= intersection_start:
                return 0.0
            
            intersection = intersection_end - intersection_start
            
            # 计算并集
            union = (gt_end_seconds - gt_start_seconds) + (user_end_seconds - user_start_seconds) - intersection
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            print(f"计算时间范围IoU时出错: {str(e)}")
            return 0.0
    
    def calculate_trajectory_segment_score(self, case: Dict, user_answers: Dict, segment: str) -> float:
        """计算轨迹预测中单个片段的得分"""
        # 获取正确答案
        correct_cam_names = case.get('correct_cam_name', [])
        correct_time_strs = case.get('correct_time_str', [])
        
        # 确定当前片段的索引
        segment_index = 0 if segment == 'first' else 1
        
        if segment_index >= len(correct_cam_names) or segment_index >= len(correct_time_strs):
            return 0.0
        
        # 检查摄像头选择是否正确
        user_camera = user_answers.get(f'{segment}_camera', '')
        gt_camera = correct_cam_names[segment_index]
        
        # 使用与check_trajectory_camera_selection相同的逻辑
        user_camera_clean = user_camera.strip()
        
        # 处理ground truth：提取摄像头名称
        gt_camera_clean = gt_camera.strip()
        if '. ' in gt_camera_clean:
            # 格式如 "C. c016" -> 提取 "c016"
            gt_camera_name = gt_camera_clean.split('. ')[1] if '. ' in gt_camera_clean else gt_camera_clean
        elif '.' in gt_camera_clean and not gt_camera_clean.startswith('c'):
            # 格式如 "C.c016" -> 提取 "c016"
            parts = gt_camera_clean.split('.')
            if len(parts) > 1:
                gt_camera_name = parts[1]
            else:
                gt_camera_name = gt_camera_clean
        else:
            # 已经是纯摄像头名称
            gt_camera_name = gt_camera_clean
        
        # 标准化摄像头名称（统一大小写）
        user_camera_clean = user_camera_clean.lower()
        gt_camera_name = gt_camera_name.lower()
        
        # 比较摄像头名称
        camera_correct = user_camera_clean == gt_camera_name
        
        # 如果摄像头选择错误，直接返回0分
        if not camera_correct:
            return 0.0
        
        # 摄像头选择正确，计算时间IoU
        user_start_time = user_answers.get(f'{segment}_start_time', '')
        user_end_time = user_answers.get(f'{segment}_end_time', '')
        gt_time_str = correct_time_strs[segment_index]
        
        time_iou = 0.0
        if user_start_time and user_end_time and gt_time_str:
            if '-' in gt_time_str:
                # 时间范围格式
                user_time_range = f"{user_start_time}-{user_end_time}"
                time_iou = self.calculate_time_range_iou_single(gt_time_str, user_time_range)
            else:
                # 单个时间点
                time_iou = self.calculate_time_iou(gt_time_str, user_start_time)
        
        # 返回时间IoU作为得分
        return time_iou
    
    def check_trajectory_camera_selection(self, case: Dict, user_answers: Dict, segment: str) -> bool:
        """检查轨迹预测中单个片段的摄像头选择是否正确"""
        # 获取正确答案
        correct_cam_names = case.get('correct_cam_name', [])
        
        # 确定当前片段的索引
        segment_index = 0 if segment == 'first' else 1
        
        if segment_index >= len(correct_cam_names):
            return False
        
        # 检查摄像头选择
        user_camera = user_answers.get(f'{segment}_camera', '')
        gt_camera = correct_cam_names[segment_index]
        
        # 处理用户答案：可能是纯摄像头名称或选项格式
        user_camera_clean = user_camera.strip()
        
        # 处理ground truth：提取摄像头名称
        gt_camera_clean = gt_camera.strip()
        if '. ' in gt_camera_clean:
            # 格式如 "C. c016" -> 提取 "c016"
            gt_camera_name = gt_camera_clean.split('. ')[1] if '. ' in gt_camera_clean else gt_camera_clean
        elif '.' in gt_camera_clean and not gt_camera_clean.startswith('c'):
            # 格式如 "C.c016" -> 提取 "c016"
            parts = gt_camera_clean.split('.')
            if len(parts) > 1:
                gt_camera_name = parts[1]
            else:
                gt_camera_name = gt_camera_clean
        else:
            # 已经是纯摄像头名称
            gt_camera_name = gt_camera_clean
        
        # 标准化摄像头名称（统一大小写）
        user_camera_clean = user_camera_clean.lower()
        gt_camera_name = gt_camera_name.lower()
        
        # 比较摄像头名称
        return user_camera_clean == gt_camera_name
    
    def calculate_time_iou(self, gt_time: str, user_time: str) -> float:
        """计算时间IoU"""
        try:
            # 解析真实时间范围
            if '-' in gt_time:
                start_time, end_time = gt_time.split('-')
                gt_start_seconds = self.time_to_seconds(start_time)
                gt_end_seconds = self.time_to_seconds(end_time)
            else:
                # 单个时间点
                gt_time_seconds = self.time_to_seconds(gt_time)
                gt_start_seconds = gt_time_seconds - 0.5  # 允许0.5秒误差
                gt_end_seconds = gt_time_seconds + 0.5
            
            # 解析用户时间
            user_seconds = self.time_to_seconds(user_time)
            
            # Calculate IoU
            intersection_start = max(gt_start_seconds, user_seconds - 0.5)
            intersection_end = min(gt_end_seconds, user_seconds + 0.5)
            
            if intersection_end <= intersection_start:
                return 0.0
            
            intersection = intersection_end - intersection_start
            union = (gt_end_seconds - gt_start_seconds) + 1.0 - intersection
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            print(f"计算时间IoU时出错: {str(e)}")
            return 0.0
    
    def extract_option_letter(self, text: str, options: list = None) -> str:
        """从文本中提取选项字母"""
        if not text:
            return ""
        
        text = text.strip()
        
        # 1. 匹配标准格式: "A. c16", "B. c16", "C. c16", "D. c16"
        pattern1 = r'^([A-D])\.\s*'
        match = re.match(pattern1, text)
        if match:
            return match.group(1)
        
        # 2. 匹配带标点的格式: "A.", "B.", "C.", "D."
        pattern2 = r'^([A-D])[.、]'
        match = re.match(pattern2, text)
        if match:
            return match.group(1)
        
        # 3. 匹配纯字母格式: "A", "B", "C", "D"
        pattern3 = r'^([A-D])$'
        match = re.match(pattern3, text)
        if match:
            return match.group(1)
        
        # 4. 匹配小写字母格式: "a", "b", "c", "d"
        pattern4 = r'^([a-d])$'
        match = re.match(pattern4, text)
        if match:
            return match.group(1).upper()
        
        # 5. 匹配包含摄像头名称的格式: "A.c16", "B.c16", "c16", "C16"
        # 如果文本包含摄像头名称，尝试提取选项字母
        if 'c' in text.lower():
            # 检查是否以选项字母开头
            pattern5 = r'^([A-D])\.?c\d+'
            match = re.match(pattern5, text)
            if match:
                return match.group(1)
            
            # 如果直接是摄像头名称，需要根据上下文判断
            # 这里可以根据具体的摄像头名称映射到选项
            # 暂时返回空字符串，需要更多上下文信息
            pass
        
        # 6. 匹配纯摄像头名称格式: "c16", "C16" 等
        # 这种情况下需要根据选项列表来判断
        if re.match(r'^c\d+$', text, re.IGNORECASE) and options:
            # 直接是摄像头名称，根据选项列表来判断
            for i, option in enumerate(options):
                if text.lower() in option.lower():
                    # 返回对应的选项字母
                    return chr(ord('A') + i)
        
        # 7. 如果提供了选项列表，尝试在选项中查找匹配
        if options:
            for i, option in enumerate(options):
                if text.lower() in option.lower() or option.lower() in text.lower():
                    return chr(ord('A') + i)
        
        return ""
    
    def time_to_seconds(self, time_str: str) -> float:
        """将时间字符串转换为秒数"""
        try:
            # 解析时间格式
            parts = time_str.split(':')
            if len(parts) != 3:
                return 0.0
            
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds_parts = parts[2].split('.')
            seconds = int(seconds_parts[0])
            milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
            
            total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
            return total_seconds
            
        except Exception as e:
            print(f"时间转换出错: {str(e)}")
            return 0.0
