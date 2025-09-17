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
        # 提取任务类型，处理不同的格式
        task_id = case.get('task_id', '')
        if task_id:
            # 处理不同的任务ID格式
            if task_id == "Next Camera Forecasting":
                task_type = "NextCameraForecasting"
            elif task_id == "Trajectory Forecasting":
                task_type = "TrajectoryForecasting"
            elif task_id == "Multi Trajectory Forecasting" or task_id == "Multi-Target Trajectory Forecasting":
                task_type = "MultiTrajectoryForecasting"
            elif ' ' in task_id:
                task_type = task_id.split()[-1]
            else:
                task_type = task_id
        else:
            task_type = ''
        
        # 检查选项答案
        option_correct = self.check_option_answers(case, user_answers)
        
        # 根据任务类型计算得分
        if task_type in ["MotionReasoning", "SpatialReasoning", "TemporalReasoning", "TimelineInference"]:
            # 选择题任务：选择正确得1分，错误得0分
            score = 1.0 if option_correct else 0.0
            accuracy_score = score
            time_score = 0.0
            
        elif task_type in ["NextCameraForecasting", "MultiTrajectoryForecasting"]:
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
            first_score = self.calculate_trajectory_segment_score(case, user_answers, 'first')
            second_score = self.calculate_trajectory_segment_score(case, user_answers, 'second')
            score = (first_score + second_score) / 2.0
            
            # 计算准确率：两个摄像头都选择正确才算正确
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
            'accuracy_score': accuracy_score,
            'time_score': time_score,
            'elapsed_time': elapsed_time,
            'is_correct': option_correct,
            'task_type': task_type
        }
    
    def check_option_answers(self, case: Dict, user_answers: Dict) -> bool:
        """
        检查选项答案是否正确
        
        Args:
            case: 题目案例数据
            user_answers: 用户答案
            
        Returns:
            是否正确
        """
        # 首先尝试从correct_cam_name字段获取正确答案
        correct_cam_names = case.get('correct_cam_name', [])
        if correct_cam_names:
            # 提取正确答案的选项字母
            gt_option = self.extract_option_letter(correct_cam_names[0])
        else:
            # 如果没有correct_cam_name，尝试ground_truth字段
            ground_truth = case.get('ground_truth', '')
            gt_option = self.extract_option_letter(ground_truth)
        
        user_options = user_answers.get('options', [])
        
        if not gt_option or not user_options:
            return False
        
        # 检查用户答案
        user_option_letters = []
        for option in user_options:
            letter = self.extract_option_letter(option)
            if letter:
                user_option_letters.append(letter)
        
        # 判断是否正确
        return gt_option in user_option_letters
    
    def calculate_time_range_iou(self, case: Dict, user_answers: Dict) -> float:
        """
        计算时间范围IoU
        
        Args:
            case: 题目案例数据
            user_answers: 用户答案
            
        Returns:
            时间IoU值 (0-1)
        """
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
        
        # 检查start_point和end_point字段（兼容旧格式）
        if 'start_point' in case and case['start_point'].get('time'):
            gt_start_time = case['start_point']['time']
            user_start_time = user_answers.get('start_time', '')
            if user_start_time:
                iou = self.calculate_time_iou(gt_start_time, user_start_time)
                time_ious.append(iou)
        
        if 'end_point' in case and case['end_point'].get('time'):
            gt_end_time = case['end_point']['time']
            user_end_time = user_answers.get('end_time', '')
            if user_end_time:
                iou = self.calculate_time_iou(gt_end_time, user_end_time)
                time_ious.append(iou)
        
        if not time_ious:
            return 0.0
        
        return np.mean(time_ious)
    
    def calculate_time_range_iou_single(self, gt_time_range: str, user_time_range: str) -> float:
        """
        计算单个时间范围的IoU
        
        Args:
            gt_time_range: 真实时间范围 (格式: "HH:MM:SS.mmm-HH:MM:SS.mmm")
            user_time_range: 用户时间范围 (格式: "HH:MM:SS.mmm-HH:MM:SS.mmm")
            
        Returns:
            时间IoU值 (0-1)
        """
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
        """
        计算轨迹预测中单个片段的得分
        
        Args:
            case: 题目案例数据
            user_answers: 用户答案
            segment: 片段标识 ('first' 或 'second')
            
        Returns:
            片段得分 (0-1)
        """
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
        
        # 比较选项（包含选项前缀，如"A. c08"）
        camera_correct = user_camera.strip() == gt_camera.strip()
        
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
        """
        检查轨迹预测中单个片段的摄像头选择是否正确
        
        Args:
            case: 题目案例数据
            user_answers: 用户答案
            segment: 片段标识 ('first' 或 'second')
            
        Returns:
            摄像头选择是否正确
        """
        # 获取正确答案
        correct_cam_names = case.get('correct_cam_name', [])
        
        # 确定当前片段的索引
        segment_index = 0 if segment == 'first' else 1
        
        if segment_index >= len(correct_cam_names):
            return False
        
        # 检查摄像头选择
        user_camera = user_answers.get(f'{segment}_camera', '')
        gt_camera = correct_cam_names[segment_index]
        
        # 比较选项（包含选项前缀，如"A. c08"）
        return user_camera.strip() == gt_camera.strip()
    
    def extract_camera_id(self, camera_text: str) -> str:
        """
        从摄像头文本中提取摄像头ID
        
        Args:
            camera_text: 摄像头文本 (格式: "A. c09" 或 "c09")
            
        Returns:
            摄像头ID
        """
        # 移除选项前缀
        if '. ' in camera_text:
            return camera_text.split('. ')[1]
        return camera_text
    
    def calculate_time_iou(self, gt_time: str, user_time: str) -> float:
        """
        计算时间IoU
        
        Args:
            gt_time: 真实时间 (格式: "HH:MM:SS.mmm-HH:MM:SS.mmm" 或 "HH:MM:SS.mmm")
            user_time: 用户输入时间 (格式: "HH:MM:SS.mmm")
            
        Returns:
            时间IoU值 (0-1)
        """
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
            
            # 计算IoU
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
    
    def extract_option_letter(self, text: str) -> str:
        """
        从文本中提取选项字母
        
        Args:
            text: 输入文本
            
        Returns:
            选项字母 (A, B, C, D等)
        """
        # 匹配选项模式
        pattern = r'^([A-D])\.'
        match = re.match(pattern, text.strip())
        if match:
            return match.group(1)
        
        # 如果没有匹配到，尝试其他模式
        pattern2 = r'([A-D])\s*[.、]'
        match = re.search(pattern2, text)
        if match:
            return match.group(1)
        
        return ""
    
    def time_to_seconds(self, time_str: str) -> float:
        """
        将时间字符串转换为秒数
        
        Args:
            time_str: 时间字符串 (格式: "HH:MM:SS.mmm")
            
        Returns:
            秒数
        """
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
    
    # 保留原有的方法以保持兼容性
    def calculate_score(self, case: Dict, user_answers: Dict, elapsed_time: float) -> Dict:
        """原有的评分方法，保持兼容性"""
        return self.calculate_score_new(case, user_answers, elapsed_time)
    
    def calculate_accuracy_score(self, case: Dict, user_answers: Dict) -> float:
        """原有的准确率计算方法，保持兼容性"""
        return 1.0 if self.check_option_answers(case, user_answers) else 0.0
    
    def check_time_answers(self, case: Dict, user_answers: Dict) -> float:
        """原有的时间答案检查方法，保持兼容性"""
        return self.calculate_time_range_iou(case, user_answers)
    
    def calculate_time_score(self, elapsed_time: float) -> float:
        """原有的时间得分计算方法，保持兼容性"""
        if elapsed_time <= 0:
            return 0.0
        
        # 使用指数衰减函数计算时间得分
        normalized_time = min(elapsed_time / self.time_threshold, 1.0)
        time_score = 0.3 * np.exp(-2 * normalized_time)
        
        return time_score
