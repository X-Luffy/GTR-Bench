#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import time
from datetime import datetime
import sys
import re
import glob
from PIL import Image
import cv2
import numpy as np
import base64

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompt.question_info import make_question_prompt
from prompt.map_info import make_map_prompt
from prompt.video_info import make_keyframe_prompt
from eval_type import get_eval_type, is_mcq_task, is_st_iou_task
from utils.scoring import ScoringSystem
from openai import OpenAI

class OpenAIModel:
    """OpenAI模型API封装"""
    
    def __init__(self, model_name: str, api_key: str, base_url: str = None):
        self.model_name = model_name
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=300.0)
        else:
            self.client = OpenAI(api_key=api_key, timeout=300.0)
        
    def generate(self, prompt: str, images: list = None, max_tokens: int = 16384, temperature: float = 0.1) -> str:
        """生成响应"""
        try:
            messages = []
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            })
            
            if images:
                for image in images:
                    messages[0]["content"].append(image)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return f"Error: {str(e)}"
        
    def generate_with_retry(self, prompt: str, images: list = None, max_retries: int = 3, max_tokens: int = 16384, temperature: float = 0.1) -> str:
        """带重试的生成响应"""
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, images, max_tokens, temperature)
            except Exception as e:
                if attempt == max_retries - 1:
                    return f"Error after {max_retries} attempts: {str(e)}"
                time.sleep(2 ** attempt)
        
        return "Error: Max retries exceeded"

def load_test_cases(data_dir):
    """Load test cases"""
    test_cases = []
    
    # Load all JSON files
    json_files = []
    for scene in ['outdoor', 'indoor']:
        scene_dir = os.path.join(data_dir, scene)
        if os.path.exists(scene_dir):
            for file in os.listdir(scene_dir):
                if file.endswith('.json'):
                    json_files.append(os.path.join(scene_dir, file))
    
    print(f"Found {len(json_files)} JSON files")
    
    for json_file in json_files:
        print(f"Loading {json_file}")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cases = data.get('cases', [])
                for case in cases:
                    # 添加场景信息
                    scene = 'outdoor' if 'outdoor' in json_file else 'indoor'
                    case['scene'] = scene
                    test_cases.append(case)
        except Exception as e:
            print(f"Error loading {json_file}: {str(e)}")
    
    print(f"Loaded {len(test_cases)} test cases")
    return test_cases

def fix_paths(case, data_dir=None, project_dir=None):
    """Fix paths"""
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    if project_dir is None:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Fix video_path
    if 'camera_images' in case:
        for camera in case['camera_images']:
            if 'video_path' in camera:
                video_path = camera['video_path']
                if video_path.startswith('./data/outdoor/') or video_path.startswith('./data/indoor/'):
                    # Handle paths with outdoor/indoor prefix
                    path_parts = video_path.replace('./data/', '').split('/')
                    if 'cityflow' in path_parts:
                        cityflow_index = path_parts.index('cityflow')
                        actual_path = '/'.join(path_parts[cityflow_index:])
                        camera['video_path'] = os.path.join(data_dir, actual_path)
                    else:
                        # For mtmmc paths, directly remove outdoor/indoor prefix
                        actual_path = '/'.join(path_parts[1:])
                        camera['video_path'] = os.path.join(data_dir, actual_path)
                elif video_path.startswith('./data/'):
                    # Replace with actual path
                    camera['video_path'] = video_path.replace('./data/', os.path.join(data_dir, '') + '/')
                elif video_path.startswith('./'):
                    # Handle other relative paths, remove outdoor/indoor prefix
                    path_parts = video_path.replace('./', '').split('/')
                    if len(path_parts) > 1 and path_parts[0] in ['outdoor', 'indoor']:
                        # Remove outdoor/indoor prefix, use cityflow path directly
                        if 'cityflow' in path_parts:
                            cityflow_index = path_parts.index('cityflow')
                            actual_path = '/'.join(path_parts[cityflow_index:])
                            camera['video_path'] = os.path.join(data_dir, actual_path)
                        else:
                            # For mtmmc paths, directly remove outdoor/indoor prefix
                            actual_path = '/'.join(path_parts[1:])
                            camera['video_path'] = os.path.join(data_dir, actual_path)
                    else:
                        camera['video_path'] = os.path.join(data_dir, video_path.replace('./', ''))
    
    # Fix map_image_path
    if 'map_image_path' in case:
        map_path = case['map_image_path']
        if map_path.startswith('./'):
            # Handle relative paths
            case['map_image_path'] = os.path.join(project_dir, map_path.replace('./', ''))
    
    return case

def create_prompt(case):
    """Create complete prompt"""
    messages = []
    
    # 1. Add map information
    if 'map_image_path' in case and os.path.exists(case['map_image_path']):
        map_messages = make_map_prompt([], [], case['map_image_path'])
        messages.extend(map_messages)
    
    # 2. Add camera video information
    if 'camera_images' in case:
        # For CausalReordering task, do not use timestamps
        task_id = case.get('task_id', '')
        with_timestamp = task_id != 'CausalReordering'
        
        video_messages = make_keyframe_prompt(case, with_timestamp=with_timestamp, with_direction=True, 
                                            with_bbox=True, is_random=False,
                                            is_resize=False, frame_limited=3)
        messages.extend(video_messages)
    
    # 3. Add question information
    question_messages = make_question_prompt(case)
    messages.extend(question_messages)
    
    return messages

def calculate_metrics(case, answer):
    """Calculate metrics - consistent with scoring design in app.py"""
    try:
        # Check if it is an error response
        if isinstance(answer, str) and answer.startswith('Error:'):
            return {
                'score': 0.0,
                'MCQacc': 0.0,
                'TimeIoU': 0.0
            }
        
        task_type = case.get('task_id', '')
        eval_type = get_eval_type(task_type)
        
        # 初始化评分系统
        scoring_system = ScoringSystem()
        
        # Parse model response
        user_answers = parse_model_answer(answer, eval_type)
        
        # Calculate score
        score_result = scoring_system.calculate_score_new(case, user_answers, 0.0)
        
        return {
            'score': score_result['score'],
            'MCQacc': score_result['MCQacc'],
            'TimeIoU': score_result['TimeIoU']
        }
        
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return {
            'score': 0.0,
            'MCQacc': 0.0,
            'TimeIoU': 0.0
        }

def extract_elements_from_string(text: str):
    """
    使用模板匹配提取字符串中的元素 - 参考之前版本的实现
    
    Args:
        text: 输入的字符串
        
    Returns:
        包含提取元素的字典
    """
    result = {}
    
    # 不提取 TF 字段
    # tf_match = re.search(r'"TF":\s*(True|False)', text)
    # if tf_match:
    #     result['TF'] = tf_match.group(1) == 'True'
    
    # 提取 answer 字段 - 处理双引号内容
    answer_match = re.search(r'"answer":\s*"([^"]*)"', text)
    if answer_match:
        result['answer'] = answer_match.group(1)
    
    # 提取 explanation 字段 - 处理多行文本
    explanation_match = re.search(r'"explanation":\s*"((?:[^"\\]|\\.)*)"\s*,', text, re.DOTALL)
    if explanation_match:
        # 处理转义字符
        explanation = explanation_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
        result['explanation'] = explanation
    
    # 提取 reasoning 字段 - 处理多行文本，可能在文本末尾
    reasoning_match = re.search(r'"reasoning":\s*"((?:[^"\\]|\\.)*)"', text, re.DOTALL)
    if reasoning_match:
        # 处理转义字符
        reasoning = reasoning_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
        result['reasoning'] = reasoning
    
    # 提取 time_duration 字段 (列表) - 支持双引号格式
    time_duration_match = re.search(r'"time_duration":\s*\[([^\]]*)\]', text)
    if time_duration_match:
        time_content = time_duration_match.group(1)
        # 提取引号中的时间范围，支持单引号和双引号
        time_items = re.findall(r'["\']([^"\']*)["\']', time_content)
        result['time_duration'] = time_items
    
    return result

def parse_model_answer(answer, eval_type):
    """解析模型回答 - 参考之前版本的实现"""
    user_answers = {}
    
    try:
        # 尝试解析JSON格式的回答
        if '{' in answer and '}' in answer:
            # 提取JSON部分
            json_start = answer.find('{')
            json_end = answer.rfind('}') + 1
            json_str = answer[json_start:json_end]
            
            try:
                # 尝试直接解析JSON
                parsed = json.loads(json_str)
            except:
                # 如果JSON解析失败，使用正则表达式提取
                parsed = extract_elements_from_string(json_str)
            
            # 提取答案 - 根据question_info.py的格式
            if 'answer' in parsed:
                answer_value = parsed['answer']
                if isinstance(answer_value, list):
                    # 处理数组格式的答案
                    user_answers['options'] = answer_value
                else:
                    # 处理单个答案
                    user_answers['options'] = [answer_value]
            
            # 提取时间信息 - 根据question_info.py的格式
            if 'time_duration' in parsed and eval_type == "ST-IoU":
                time_durations = parsed['time_duration']
                if isinstance(time_durations, list):
                    for i, time_duration in enumerate(time_durations):
                        if '-' in time_duration:
                            start_time, end_time = time_duration.split('-')
                            user_answers[f'time_range_{i}_start'] = start_time.strip()
                            user_answers[f'time_range_{i}_end'] = end_time.strip()
                        else:
                            user_answers[f'time_range_{i}'] = time_duration.strip()
                else:
                    # 单个时间范围
                    time_duration = time_durations
                    if '-' in time_duration:
                        start_time, end_time = time_duration.split('-')
                        user_answers[f'time_range_0_start'] = start_time.strip()
                        user_answers[f'time_range_0_end'] = end_time.strip()
                    else:
                        user_answers[f'time_range_0'] = time_duration.strip()
            
            # 不提取TF字段
            # if 'TF' in parsed:
            #     user_answers['TF'] = parsed['TF']
        
        # 如果没有解析到JSON，尝试从文本中提取选项
        if not user_answers:
            # 简单的文本匹配
            if isinstance(answer, str):
                answer_lower = answer.lower()
                if 'a.' in answer_lower or 'option a' in answer_lower:
                    user_answers['options'] = ['A']
                elif 'b.' in answer_lower or 'option b' in answer_lower:
                    user_answers['options'] = ['B']
                elif 'c.' in answer_lower or 'option c' in answer_lower:
                    user_answers['options'] = ['C']
                elif 'd.' in answer_lower or 'option d' in answer_lower:
                    user_answers['options'] = ['D']
    
    except Exception as e:
        print(f"Error parsing model answer: {str(e)}")
        print(f"Answer content: {answer[:200]}...")
    
    return user_answers

def save_individual_prompt_file(messages, case, model_response, metrics, result_dir, model_name):
    """Save complete prompt for single case to file"""
    os.makedirs(result_dir, exist_ok=True)
    
    # Create filename, add model_name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    case_id = case.get('case_id', 'unknown')
    task_id = case.get('task_id', 'unknown')
    # Clean special characters in model_name for filename
    clean_model_name = model_name.replace('-', '_').replace('.', '_')
    filename = f"prompt_{clean_model_name}_{case_id}_{task_id}_{timestamp}.json"
    # Create prompt subdirectory
    prompt_dir = os.path.join(result_dir, "prompt")
    os.makedirs(prompt_dir, exist_ok=True)
    filepath = os.path.join(prompt_dir, filename)
    
    # 准备完整的对话消息
    complete_messages = []
    
    # 添加用户消息（包含所有prompt内容）
    user_content = []
    for message in messages:
        if message['type'] == 'text':
            user_content.append({
                'type': 'text',
                'text': message['text']
            })
        elif message['type'] == 'image_url':
            user_content.append({
                'type': 'image_url',
                'image_url': message['image_url']
            })
    
    complete_messages.append({
        "role": "user",
        "content": user_content
    })
    
    # 添加模型回答
    if model_response is not None:
        complete_messages.append({
            "role": "assistant",
            "content": model_response
        })
    
    # Parse model response，提取elements
    parsed_elements = {}
    if model_response is not None:
        try:
            task_type = case.get('task_id', '')
            eval_type = get_eval_type(task_type)
            parsed_elements = parse_model_answer(model_response, eval_type)
        except Exception as e:
            print(f"Error parsing model response: {str(e)}")
            parsed_elements = {}
    
    # Handle ground_truth field
    if 'ground_truth' in case:
        ground_truth = case['ground_truth']
    else:
        ground_truth = {
            "correct_cam_name": case.get('correct_cam_name', ''),
            "correct_time_str": case.get('correct_time_str', [])
        }
    
    # Handle time_duration field
    time_duration = []
    i = 0
    while f'time_range_{i}_start' in parsed_elements and f'time_range_{i}_end' in parsed_elements:
        time_duration.append(f"{parsed_elements[f'time_range_{i}_start']}-{parsed_elements[f'time_range_{i}_end']}")
        i += 1
    
    if not time_duration and 'time_duration' in parsed_elements:
        time_duration = parsed_elements['time_duration']
    
    # 准备导出数据 - 取消case_info字段
    export_data = {
        "metadata": {
            "case_id": case_id,
            "task_id": task_id,
            "model_name": model_name,
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat(),
            "type": "openai_conversation_with_evaluation"
        },
        "messages": complete_messages,
        "evaluation": {
            "response": {
                "model_answer": model_response,
                "answer": parsed_elements.get('options', []),
                "time_duration": time_duration,
                "ground_truth": ground_truth
            },
            "metrics": {
                "score": round(metrics['score'], 3),
                "MCQacc": round(metrics['MCQacc'], 3),
                "TimeIoU": round(metrics['TimeIoU'], 3)
            }
        }
    }
    
    # Save to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 完整对话记录已导出到: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ 对话记录导出失败: {str(e)}")
        return None

def evaluate_model(model_name, api_key, test_cases, result_dir, base_url=None, max_tokens=16384, temperature=0.1):
    """Evaluate model"""
    # Initialize model
    model = OpenAIModel(model_name, api_key, base_url)
    
    results = []
    total_cases = len(test_cases)
    
    print(f"Starting evaluation with {model_name}")
    print(f"Total cases: {total_cases}")
    
    # Create unified timestamp for all files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, case in enumerate(test_cases):
        print(f"Processing case {i+1}/{total_cases}: {case.get('case_id', 'unknown')}")
        
        try:
            # Fix paths
            case = fix_paths(case, args.data_dir, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Create prompt
            messages = create_prompt(case)
            
            # Prepare image data
            images = []
            prompt_text = ""
            
            for message in messages:
                if message['type'] == 'text':
                    prompt_text += message['text'] + "\n"
                elif message['type'] == 'image_url':
                    images.append({
                        'type': 'image_url',
                        'image_url': message['image_url']
                    })
            
            # Call model
            answer = model.generate_with_retry(prompt_text, images, max_tokens=max_tokens, temperature=temperature)
            
            # Calculate metrics
            metrics = calculate_metrics(case, answer)
            
            # Save complete prompt to separate file
            save_individual_prompt_file(messages, case, answer, metrics, result_dir, model_name)
            
            # Handle ground_truth field
            if 'ground_truth' in case:
                ground_truth = case['ground_truth']
            else:
                ground_truth = {
                    'correct_cam_name': case.get('correct_cam_name', ''),
                    'correct_time_str': case.get('correct_time_str', [])
                }
            
            # Parse model response，提取elements
            parsed_elements = {}
            if answer is not None:
                try:
                    task_type = case.get('task_id', '')
                    eval_type = get_eval_type(task_type)
                    parsed_elements = parse_model_answer(answer, eval_type)
                except Exception as e:
                    print(f"Error parsing model response: {str(e)}")
                    parsed_elements = {}
            
            # Handle time_duration field
            time_duration = []
            j = 0
            while f'time_range_{j}_start' in parsed_elements and f'time_range_{j}_end' in parsed_elements:
                time_duration.append(f"{parsed_elements[f'time_range_{j}_start']}-{parsed_elements[f'time_range_{j}_end']}")
                j += 1
            
            if not time_duration and 'time_duration' in parsed_elements:
                time_duration = parsed_elements['time_duration']
            
            result = {
                'case_id': case.get('case_id', ''),
                'scene': case.get('scene', ''),
                'task_id': case.get('task_id', ''),
                'question': case.get('question', ''),
                'response': {
                    'model_answer': answer,
                    'answer': parsed_elements.get('options', []),
                    'time_duration': time_duration,
                    'ground_truth': ground_truth
                },
                'metrics': {
                    'score': round(metrics['score'], 3),
                    'MCQacc': round(metrics['MCQacc'], 3),
                    'TimeIoU': round(metrics['TimeIoU'], 3)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            
            # Display progress
            if (i + 1) % 10 == 0:
                print(f"Completed {i+1}/{total_cases} cases")
                
        except Exception as e:
            print(f"Error processing case {i+1}: {str(e)}")
            # Handle ground_truth field
            if 'ground_truth' in case:
                ground_truth = case['ground_truth']
            else:
                ground_truth = {
                    'correct_cam_name': case.get('correct_cam_name', ''),
                    'correct_time_str': case.get('correct_time_str', [])
                }
            
            result = {
                'case_id': case.get('case_id', ''),
                'scene': case.get('scene', ''),
                'task_id': case.get('task_id', ''),
                'question': case.get('question', ''),
                'response': {
                    'model_answer': '',
                    'answer': [],
                    'time_duration': [],
                    'ground_truth': ground_truth
                },
                'metrics': {
                    'score': 0.000,
                    'MCQacc': 0.000,
                    'TimeIoU': 0.000
                },
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            results.append(result)
    
    # Save consolidated result file
    # Clean special characters in model_name for filename
    clean_model_name = model_name.replace('-', '_').replace('.', '_')
    result_file = os.path.join(result_dir, f"{clean_model_name}_{timestamp}.json")
    
    # Save evaluation results
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {result_file}")
    
    # Calculate overall statistics
    total_cases = len(results)
    correct_cases = sum(1 for r in results if r.get('metrics', {}).get('MCQacc', 0) > 0)
    accuracy = correct_cases / total_cases if total_cases > 0 else 0
    avg_score = sum(r.get('metrics', {}).get('score', 0) for r in results) / total_cases if total_cases > 0 else 0
    avg_time_score = sum(r.get('metrics', {}).get('TimeIoU', 0) for r in results) / total_cases if total_cases > 0 else 0
    
    print(f"\nEvaluation Summary:")
    print(f"Total cases: {total_cases}")
    print(f"Correct cases: {correct_cases}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Average Score: {avg_score:.3f}")
    print(f"Average TimeIoU: {avg_time_score:.3f}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Evaluate models on GTR-Bench dataset')
    parser.add_argument('--model', required=True, help='Model name (e.g., gpt-4o, claude-sonnet-4-20250514-thinking)')
    parser.add_argument('--api-key', required=True, help='OpenAI API key')
    parser.add_argument('--data-dir', default='../data', help='Data directory path')
    parser.add_argument('--result-dir', default='./result', help='Result directory path')
    parser.add_argument('--max-cases', type=int, help='Maximum number of cases to evaluate')
    parser.add_argument('--base-url', help='Custom base URL for API (e.g., https://api.apiyi.com/v1)')
    parser.add_argument('--case-id', nargs='+', help='Specific case ID(s) to test (can specify multiple)')
    parser.add_argument('--scene', help='Filter by scene (indoor/outdoor)')
    parser.add_argument('--task-type', help='Filter by task type (e.g., ArrivalTimeInterval, NextSpotForecasting)')
    parser.add_argument('--output-dir', help='Output directory for results (overrides --result-dir)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--max-tokens', type=int, default=16384, help='Maximum tokens for model response')
    parser.add_argument('--temperature', type=float, default=0.1, help='Temperature for model response')
    
    args = parser.parse_args()
    
    # Set output directory
    if args.output_dir:
        args.result_dir = args.output_dir
    
    # Create result directory
    os.makedirs(args.result_dir, exist_ok=True)
    
    # Load test cases
    test_cases = load_test_cases(args.data_dir)
    
    # Apply filters
    if args.scene:
        test_cases = [case for case in test_cases if case.get('scene') == args.scene]
        if args.verbose:
            print(f"Filtered by scene: {args.scene} ({len(test_cases)} cases)")
    
    if args.task_type:
        test_cases = [case for case in test_cases if case.get('task_id') == args.task_type]
        if args.verbose:
            print(f"Filtered by task type: {args.task_type} ({len(test_cases)} cases)")
    
    # Limit number of test cases or specify specific cases
    if args.case_id:
        # Find specified cases
        filtered_cases = []
        for case_id in args.case_id:
            found_cases = [case for case in test_cases if case.get('case_id') == case_id]
            if found_cases:
                filtered_cases.extend(found_cases)
            else:
                print(f"Warning: Case ID {case_id} not found!")
        
        if not filtered_cases:
            print("No valid case IDs found!")
            return
        
        test_cases = filtered_cases
        print(f"Testing specific cases: {args.case_id}")
    elif args.max_cases:
        # If scene and task_type not specified, this is "all scenes-tasks" mode
        if not args.scene and not args.task_type:
            # Group by scene and task type, take max_cases from each combination
            grouped_cases = {}
            for case in test_cases:
                scene = case.get('scene', 'unknown')
                task_id = case.get('task_id', 'unknown')
                key = f"{scene}_{task_id}"
                if key not in grouped_cases:
                    grouped_cases[key] = []
                grouped_cases[key].append(case)
            
            # Take max_cases from each combination
            selected_cases = []
            for key, cases in grouped_cases.items():
                selected_cases.extend(cases[:args.max_cases])
                print(f"Selected {min(len(cases), args.max_cases)} cases from {key}")
            
            test_cases = selected_cases
            print(f"Total selected cases: {len(test_cases)}")
        else:
            # Specific scene-task mode, directly limit quantity
            test_cases = test_cases[:args.max_cases]
            print(f"Limited to {len(test_cases)} cases for testing")
    
    # 评估模型
    results = evaluate_model(args.model, args.api_key, test_cases, args.result_dir, args.base_url, args.max_tokens, args.temperature)
    
    print("Evaluation completed!")

if __name__ == "__main__":
    main()
