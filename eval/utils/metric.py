#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from typing import Dict, Any, List, Tuple

def parse_time_str(time_str: str) -> float:
    """解析时间字符串为秒数"""
    try:
        if not time_str or time_str.strip() == '':
            return 0.0
        
        # 处理 HH:MM:SS.mmm 格式
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds_parts = parts[2].split('.')
                seconds = int(seconds_parts[0])
                milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
                return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        
        # 处理纯数字（秒）
        return float(time_str)
    except:
        return 0.0

def parse_time_range(time_range: str) -> Tuple[float, float]:
    """解析时间范围字符串"""
    try:
        if '-' in time_range:
            start_str, end_str = time_range.split('-', 1)
            start_time = parse_time_str(start_str.strip())
            end_time = parse_time_str(end_str.strip())
            return start_time, end_time
        else:
            time_val = parse_time_str(time_range.strip())
            return time_val, time_val
    except:
        return 0.0, 0.0

def calculate_accuracy_score(case: Dict[str, Any], user_answers: Dict[str, Any]) -> float:
    """计算准确率得分"""
    try:
        # 获取正确答案 - 从response中的ground_truth字段获取
        response = case.get('response', {})
        ground_truth = response.get('ground_truth', {})
        
        # 获取用户答案
        user_options = user_answers.get('answer', [])
        if not isinstance(user_options, list):
            user_options = [user_options]
        
        if isinstance(ground_truth, dict):
            # 字典格式：包含correct_cam_name字段
            correct_cam_names = ground_truth.get('correct_cam_name', [])
            # 检查摄像头选择是否正确
            for user_option in user_options:
                user_option_str = str(user_option).strip()
                for correct_cam in correct_cam_names:
                    if is_option_match(user_option_str, correct_cam):
                        return 1.0
        elif isinstance(ground_truth, str):
            # 字符串格式：直接比较
            for user_option in user_options:
                user_option_str = str(user_option).strip()
                if is_option_match(user_option_str, ground_truth):
                    return 1.0
        
        return 0.0
        
    except Exception as e:
        print(f"Error calculating accuracy score: {str(e)}")
        return 0.0

def is_option_match(user_answer: str, ground_truth: str) -> bool:
    """检查选项是否匹配，支持多种格式"""
    try:
        user_answer = user_answer.strip()
        ground_truth = ground_truth.strip()
        
        # 提取ground truth中的摄像头名称
        if '. ' in ground_truth:
            # 格式如 "A. c012" -> 提取 "c012"
            gt_camera = ground_truth.split('. ')[1]
            gt_option = ground_truth.split('. ')[0]
        elif '.' in ground_truth and not ground_truth.startswith('c'):
            # 格式如 "A.c012" -> 提取 "c012"
            parts = ground_truth.split('.')
            if len(parts) > 1:
                gt_camera = parts[1]
                gt_option = parts[0]
            else:
                gt_camera = ground_truth
                gt_option = ""
        else:
            # 已经是纯摄像头名称
            gt_camera = ground_truth
            gt_option = ""
        
        # 标准化
        user_answer_lower = user_answer.lower()
        gt_camera_lower = gt_camera.lower()
        gt_option_lower = gt_option.lower()
        
        # 匹配规则：
        # 1. 完全匹配
        if user_answer_lower == ground_truth.lower():
            return True
        
        # 2. 选项字母匹配 (A, a, A., a.)
        if user_answer_lower in ['a', 'b', 'c', 'd'] and gt_option_lower == user_answer_lower:
            return True
        if user_answer_lower in ['a.', 'b.', 'c.', 'd.'] and gt_option_lower == user_answer_lower[:-1]:
            return True
        
        # 3. 摄像头名称匹配 (c012, C012)
        if user_answer_lower == gt_camera_lower:
            return True
        
        # 4. 包含匹配 - 只有当用户答案是完整摄像头名称时才匹配
        if len(user_answer_lower) >= 3 and (gt_camera_lower in user_answer_lower or user_answer_lower in gt_camera_lower):
            return True
        
        return False
        
    except Exception as e:
        print(f"Error in option matching: {str(e)}")
        return False

def calculate_time_score(case: Dict[str, Any], user_answers: Dict[str, Any]) -> float:
    """计算时间得分"""
    try:
        # 获取正确答案时间 - 从response中的ground_truth字段获取
        response = case.get('response', {})
        ground_truth = response.get('ground_truth', {})
        if isinstance(ground_truth, dict):
            correct_time_strs = ground_truth.get('correct_time_str', [])
        else:
            correct_time_strs = []
        
        if not correct_time_strs:
            return 1.0  # 没有时间要求，给满分
        
        # 获取用户时间范围
        user_time_durations = user_answers.get('time_duration', [])
        if not user_time_durations:
            return 0.0
        
        # 计算时间IoU
        total_iou = 0.0
        for i, correct_time_str in enumerate(correct_time_strs):
            if i >= len(user_time_durations):
                break
                
            user_time_range = user_time_durations[i]
            if '-' not in user_time_range:
                continue
                
            # 计算时间范围IoU
            iou = calculate_time_range_iou(correct_time_str, user_time_range)
            total_iou += iou
        
        return total_iou / len(correct_time_strs) if correct_time_strs else 0.0
        
    except Exception as e:
        print(f"Error calculating time score: {str(e)}")
        return 0.0

def calculate_time_range_iou(gt_time_range: str, user_time_range: str) -> float:
    """计算时间范围IoU"""
    try:
        # 解析时间范围
        gt_start, gt_end = parse_time_range(gt_time_range)
        user_start, user_end = parse_time_range(user_time_range)
        
        # 计算交集
        intersection_start = max(gt_start, user_start)
        intersection_end = min(gt_end, user_end)
        
        if intersection_end <= intersection_start:
            return 0.0
        
        intersection = intersection_end - intersection_start
        union = (gt_end - gt_start) + (user_end - user_start) - intersection
        
        return intersection / union if union > 0 else 0.0
        
    except Exception as e:
        print(f"Error calculating time range IoU: {str(e)}")
        return 0.0

def calculate_st_iou_score(case: Dict[str, Any], answer: str) -> float:
    """计算ST-IoU得分（用于预测任务）"""
    try:
        # 获取正确答案
        correct_cam_names = case.get('correct_cam_name', [])
        correct_time_strs = case.get('correct_time_str', [])
        
        if not correct_cam_names or not correct_time_strs:
            return calculate_accuracy_score(case, answer)
        
        # 检查摄像头选择
        answer_lower = answer.lower().strip()
        camera_correct = False
        for correct_cam in correct_cam_names:
            if correct_cam.lower().strip() in answer_lower:
                camera_correct = True
                break
        
        if not camera_correct:
            return 0.0
        
        # 计算时间IoU
        time_score = calculate_time_score(case, answer)
        
        # ST-IoU = 摄像头正确性 * 时间IoU
        return time_score
        
    except Exception as e:
        print(f"Error calculating ST-IoU score: {str(e)}")
        return 0.0

def calculate_metrics(case: Dict[str, Any], user_answers: Dict[str, Any]) -> Dict[str, float]:
    """计算综合指标 - 与app.py中的得分设计保持一致"""
    try:
        task_type = case.get('task_id', '')  # 修复：使用task_id而不是task_type
        
        # 检查选项答案是否正确
        accuracy_score = calculate_accuracy_score(case, user_answers)
        
        # 根据任务类型计算得分
        if task_type in ["MotionState", "GeoLocation", "ArrivalTimeInterval", "CausalReordering"]:
            # 选择题任务：选择正确得1分，错误得0分
            score = 1.0 if accuracy_score > 0 else 0.0
            time_score = 0.0
            
        elif task_type in ["NextSpotForecasting", "MultiTargetTrajectoryForecasting"]:
            # 选择题+时间范围任务：选择正确才计算TimeIoU
            if accuracy_score > 0:
                time_score = calculate_time_score(case, user_answers)
                score = time_score
            else:
                score = 0.0
                time_score = 0.0
                
        elif task_type == "TrajectoryForecasting":
            # 轨迹预测任务：独立计算两段得分并求平均
            first_score = calculate_trajectory_segment_score(case, user_answers, 'first')
            second_score = calculate_trajectory_segment_score(case, user_answers, 'second')
            score = (first_score + second_score) / 2.0
            
            # Calculate accuracy：每个摄像头选择正确得0.5分
            first_camera_correct = check_trajectory_camera_selection(case, user_answers, 'first')
            second_camera_correct = check_trajectory_camera_selection(case, user_answers, 'second')
            accuracy_score = (0.5 if first_camera_correct else 0.0) + (0.5 if second_camera_correct else 0.0)
            time_score = score
            
        else:
            # 默认情况
            score = 1.0 if accuracy_score > 0 else 0.0
            time_score = 0.0
        
        return {
            'score': round(score, 4),
            'MCQacc': round(accuracy_score, 4),
            'TimeIoU': round(time_score, 4)
        }
        
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return {
            'score': 0.0,
            'MCQacc': 0.0,
            'TimeIoU': 0.0
        }

def calculate_trajectory_segment_score(case: Dict[str, Any], user_answers: Dict[str, Any], segment: str) -> float:
    """计算轨迹预测中单个片段的得分"""
    try:
        # 获取正确答案 - 从response中的ground_truth字段获取
        response = case.get('response', {})
        ground_truth = response.get('ground_truth', {})
        if isinstance(ground_truth, dict):
            correct_cam_names = ground_truth.get('correct_cam_name', [])
            correct_time_strs = ground_truth.get('correct_time_str', [])
        else:
            correct_cam_names = []
            correct_time_strs = []
        
        # 确定当前片段的索引
        segment_index = 0 if segment == 'first' else 1
        
        if segment_index >= len(correct_cam_names) or segment_index >= len(correct_time_strs):
            return 0.0
        
        # 检查摄像头选择是否正确
        user_options = user_answers.get('answer', [])
        if not isinstance(user_options, list) or len(user_options) <= segment_index:
            return 0.0
        
        user_camera = str(user_options[segment_index]).strip()
        gt_camera = correct_cam_names[segment_index]
        
        # 检查摄像头选择
        camera_correct = is_option_match(user_camera, gt_camera)
        
        # 如果摄像头选择错误，直接返回0分
        if not camera_correct:
            return 0.0
        
        # 摄像头选择正确，计算时间IoU
        gt_time_str = correct_time_strs[segment_index]
        user_time_durations = user_answers.get('time_duration', [])
        
        if segment_index >= len(user_time_durations):
            return 0.0
        
        user_time_range = user_time_durations[segment_index]
        if '-' not in user_time_range:
            return 0.0
        
        # 计算时间范围IoU
        return calculate_time_range_iou(gt_time_str, user_time_range)
        
    except Exception as e:
        print(f"Error calculating trajectory segment score: {str(e)}")
        return 0.0

def check_trajectory_camera_selection(case: Dict[str, Any], user_answers: Dict[str, Any], segment: str) -> bool:
    """检查轨迹预测中单个片段的摄像头选择是否正确"""
    try:
        # 获取正确答案 - 从response中的ground_truth字段获取
        response = case.get('response', {})
        ground_truth = response.get('ground_truth', {})
        if isinstance(ground_truth, dict):
            correct_cam_names = ground_truth.get('correct_cam_name', [])
        else:
            correct_cam_names = []
        
        # 确定当前片段的索引
        segment_index = 0 if segment == 'first' else 1
        
        if segment_index >= len(correct_cam_names):
            return False
        
        # 获取用户答案
        user_options = user_answers.get('answer', [])
        if not isinstance(user_options, list) or len(user_options) <= segment_index:
            return False
        
        user_camera = str(user_options[segment_index]).strip()
        gt_camera = correct_cam_names[segment_index]
        
        # 使用选项匹配函数
        return is_option_match(user_camera, gt_camera)
        
    except Exception as e:
        print(f"Error checking trajectory camera selection: {str(e)}")
        return False
