import streamlit as st
import json
import os
import cv2
import numpy as np
from PIL import Image
import time
from datetime import datetime
import pandas as pd
import subprocess
import threading
import queue
from utils.data_loader import DataLoader
from utils.video_processor import VideoProcessor
from utils.scoring import ScoringSystem
from components.question_display import QuestionDisplay
from components.result_display import ResultDisplay

def seconds_to_time_format(seconds):
    """
    将秒数转换为12:00:00.000格式
    
    Args:
        seconds: 秒数（浮点数）
        
    Returns:
        格式化的时间字符串
    """
    # 计算小时、分钟、秒和毫秒
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    
    # 格式化为12:00:00.000格式
    return f"12:{minutes:02d}:{secs:02d}.{milliseconds:03d}"

# 设置页面配置
st.set_page_config(
    page_title="人类水平评估系统",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .camera-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .camera-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .submit-button {
        background-color: #28a745;
        color: white;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
    }
    .submit-button:hover {
        background-color: #218838;
    }
    .result-correct {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .result-incorrect {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .task-info {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 初始化session state
    if 'current_task' not in st.session_state:
        st.session_state.current_task = None
    if 'current_case_index' not in st.session_state:
        st.session_state.current_case_index = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = DataLoader()
    if 'video_processor' not in st.session_state:
        st.session_state.video_processor = VideoProcessor()
    if 'scoring_system' not in st.session_state:
        st.session_state.scoring_system = ScoringSystem()
    
    # 评估功能相关状态
    if 'eval_process' not in st.session_state:
        st.session_state.eval_process = None
    if 'eval_output' not in st.session_state:
        st.session_state.eval_output = []
    if 'eval_progress' not in st.session_state:
        st.session_state.eval_progress = 0
    if 'eval_total' not in st.session_state:
        st.session_state.eval_total = 0
    if 'eval_status' not in st.session_state:
        st.session_state.eval_status = "idle"  # idle, running, completed, error

    # 主标题
    st.markdown('<h1 class="main-header">🎯 人类水平评估系统</h1>', unsafe_allow_html=True)

    # 侧边栏配置
    with st.sidebar:
        st.markdown('<h3 class="sub-header">📋 系统配置</h3>', unsafe_allow_html=True)
        
        # 场景选择
        scene = st.selectbox(
            "选择场景",
            ["outdoor", "indoor"],
            index=0
        )
        
        # 任务类型选择
        task_types = {
            "outdoor": [
                "MotionState",
                "GeoLocation", 
                "ArrivalTimeInterval",
                "CausalReordering",
                "TrajectoryForecasting",
                "NextSpotForecasting",
                "MultiTrajectoryForecasting"
            ],
            "indoor": [
                "MotionState",
                "GeoLocation",
                "ArrivalTimeInterval", 
                "CausalReordering",
                "TrajectoryForecasting",
                "NextSpotForecasting",
                "MultiTrajectoryForecasting"
            ]
        }
        
        task_type = st.selectbox(
            "选择任务类型",
            task_types[scene],
            index=0
        )
        
        # 显示任务说明
        task_descriptions = {
            "MotionState": "运动状态推理 - 选择题",
            "GeoLocation": "地理位置推理 - 选择题", 
            "ArrivalTimeInterval": "到达时间间隔推理 - 选择题",
            "CausalReordering": "因果重排序推理 - 选择题",
            "NextSpotForecasting": "下一位置预测 - 选择题 + 时间范围填空",
            "TrajectoryForecasting": "轨迹预测 - 预测两个摄像头 + 时间范围",
            "MultiTrajectoryForecasting": "多轨迹预测 - 选择题 + 时间范围填空"
        }
        
        if task_type in task_descriptions:
            st.info(f"📝 {task_descriptions[task_type]}")
        
        # 加载数据
        if st.button("🔄 加载题目数据"):
            try:
                st.session_state.data_loader.load_data(scene, task_type)
                st.session_state.current_task = f"{scene}_{task_type}"
                st.session_state.current_case_index = 0
                st.session_state.user_answers = {}
                st.session_state.question_started = False
                st.session_state.answer_submitted = False
                st.session_state.start_time = None
                # 清除其他界面状态，确保回到主界面
                if 'show_results' in st.session_state:
                    del st.session_state.show_results
                if 'show_eval' in st.session_state:
                    del st.session_state.show_eval
                st.success(f"✅ 成功加载 {scene} - {task_type} 题目数据")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 加载数据失败: {str(e)}")
        
        st.markdown("---")
        
        # 显示统计信息
        if st.session_state.data_loader.data:
            st.markdown('<h4>📊 统计信息</h4>', unsafe_allow_html=True)
            total_cases = len(st.session_state.data_loader.data.get('cases', []))
            st.write(f"总题目数: {total_cases}")
            st.write(f"当前题目: {st.session_state.current_case_index + 1}")
            
            # 题目导航
            if total_cases > 0:
                case_index = st.slider(
                    "选择题目",
                    0, total_cases - 1,
                    st.session_state.current_case_index
                )
                if case_index != st.session_state.current_case_index:
                    st.session_state.current_case_index = case_index
                    st.session_state.user_answers = {}
                    st.session_state.question_started = False
                    st.session_state.answer_submitted = False
                    st.session_state.start_time = None
                    st.rerun()
        
        st.markdown("---")
        
        # 查看结果
        if st.button("📈 查看答题结果"):
            if st.session_state.results:
                show_results_summary()
            else:
                st.warning("暂无答题记录")
        
        st.markdown("---")
        
        # 模型评估功能
        st.markdown('<h4>🤖 模型评估</h4>', unsafe_allow_html=True)
        if st.button("🚀 启动模型评估"):
            st.session_state.show_eval = True
            st.rerun()
        
        # 查看评估结果
        if st.button("📈 查看评估结果"):
            st.session_state.show_results = True
            st.rerun()

    # 主内容区域
    if 'show_eval' in st.session_state and st.session_state.show_eval:
        # 显示模型评估界面
        display_eval_interface()
    elif 'show_results' in st.session_state and st.session_state.show_results:
        # 显示结果可视化界面
        display_results_visualization()
    elif st.session_state.data_loader.data and st.session_state.current_task:
        # 显示正常答题界面
        display_current_question()
    else:
        st.info("👈 请在左侧选择场景和任务类型，然后加载题目数据")

def display_current_question():
    """显示当前题目"""
    data = st.session_state.data_loader.data
    cases = data.get('cases', [])
    
    if not cases or st.session_state.current_case_index >= len(cases):
        st.error("题目数据加载失败或索引超出范围")
        return
    
    current_case = cases[st.session_state.current_case_index]
    # 提取任务类型，处理不同的格式
    task_id = current_case.get('task_id', '')
    if task_id:
        # 直接使用task_id作为任务类型
        task_type = task_id
    else:
        task_type = ''
    
    # 初始化答题状态
    if 'question_started' not in st.session_state:
        st.session_state.question_started = False
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    
    # 显示题目信息
    st.markdown(f'<h2 class="sub-header">📝 题目 {st.session_state.current_case_index + 1}</h2>', unsafe_allow_html=True)
    
    # 显示任务类型信息
    task_descriptions = {
        "MotionState": "🎯 运动状态推理任务 - 请根据提供的视频信息推理目标的运动状态",
        "GeoLocation": "🎯 地理位置推理任务 - 请根据提供的视频信息推理目标的空间位置关系",
        "ArrivalTimeInterval": "🎯 到达时间间隔推理任务 - 请根据提供的视频信息推理目标的时间顺序",
        "CausalReordering": "🎯 因果重排序推理任务 - 请根据提供的视频信息推理目标的因果关系",
        "NextSpotForecasting": "🎯 下一位置预测任务 - 请预测目标接下来经过的位置和时间范围",
        "TrajectoryForecasting": "🎯 轨迹预测任务 - 请预测目标接下来经过的两个位置和对应时间范围",
        "MultiTrajectoryForecasting": "🎯 多轨迹预测任务 - 请预测多个目标的轨迹和时间范围"
    }
    
    if task_type in task_descriptions:
        st.markdown(f'<div class="task-info">{task_descriptions[task_type]}</div>', unsafe_allow_html=True)
    
    # 自动开始答题（不需要按钮）
    if not st.session_state.question_started:
        st.session_state.question_started = True
        st.session_state.start_time = time.time()
    
    # 如果答案已提交，显示结果但不阻止继续操作
    if st.session_state.answer_submitted:
        # 答案已提交，但用户可以继续查看题目和结果
        pass
    
    # 显示地图
    if current_case.get('map_image_path'):
        # 修改地图路径处理
        map_path = current_case['map_image_path']
        if map_path.startswith('./'):
            # 相对于项目根目录的路径，现在路径已经包含了data目录
            map_path = os.path.join(
                os.getcwd(),
                map_path.replace('./', '')
            )
        
        if os.path.exists(map_path):
            st.markdown('<h4>🗺️ 场景地图</h4>', unsafe_allow_html=True)
            try:
                map_image = Image.open(map_path)
                # 创建地图容器，限制最大尺寸
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        # 限制地图大小
                        st.image(map_image, use_container_width=True)
            except Exception as e:
                st.error(f"无法加载地图图像: {str(e)}")
        else:
            st.warning(f"地图文件不存在: {map_path}")
    
    # 显示摄像头图像
    camera_images = current_case.get('camera_images', [])
    if camera_images:
        st.markdown('<h4>📹 摄像头图像</h4>', unsafe_allow_html=True)
        
        # 为每个摄像头显示图像
        for i, camera in enumerate(camera_images):
            camera_id = camera.get('camera_id', f'Camera_{i}')
            
            # 对于CausalReordering任务，不显示时间范围
            if task_type == "CausalReordering":
                expander_title = f"📹 摄像头 {camera_id}"
            else:
                # 转换时间格式
                start_time_str = seconds_to_time_format(camera['start_timestamp'])
                end_time_str = seconds_to_time_format(camera['end_timestamp'])
                expander_title = f"📹 摄像头 {camera_id} (时间: {start_time_str} - {end_time_str})"
            
            with st.expander(expander_title):
                # 显示视频路径信息
                video_path = camera.get('video_path', '')
                
                # 处理相对路径，转换为绝对路径
                if video_path.startswith('./'):
                    # 相对于项目根目录的路径，现在路径已经包含了data目录
                    video_path = os.path.join(
                        os.getcwd(),
                        video_path.replace('./', '')
                    )
                
                st.write(f"**视频路径:** {video_path}")
                
                # 检查视频文件是否存在
                if os.path.exists(video_path):
                    st.success("✅ 视频文件存在")
                    
                    # 从视频中提取帧
                    frames = st.session_state.video_processor.extract_frames(
                        video_path,
                        camera['frame_ids'],
                        camera['bboxes']
                    )
                    
                    if frames:
                        # 显示3张均匀选择的帧
                        cols = st.columns(3)
                        for j, frame in enumerate(frames):
                            with cols[j]:
                                st.image(frame, caption=f"帧 {camera['frame_ids'][j]}", use_container_width=True)
                    else:
                        st.warning(f"无法从视频中提取帧")
                        
                        # 尝试获取视频信息
                        video_info = st.session_state.video_processor.get_video_info(video_path)
                        if video_info:
                            st.write("**视频信息:**")
                            st.write(f"- 总帧数: {video_info['frame_count']}")
                            st.write(f"- 帧率: {video_info['fps']:.2f}")
                            st.write(f"- 分辨率: {video_info['width']}x{video_info['height']}")
                            st.write(f"- 时长: {video_info['duration']:.2f}秒")
                        
                        # 显示请求的帧ID
                        st.write(f"**请求的帧ID:** {camera['frame_ids']}")
                        
                else:
                    st.error(f"❌ 视频文件不存在: {video_path}")
    
    # 显示问题
    st.markdown('<h4>❓ 问题</h4>', unsafe_allow_html=True)
    question = current_case.get('question', '')
    st.markdown(f'<div class="question-container">{question}</div>', unsafe_allow_html=True)
    
    # 根据任务类型显示不同的答题界面
    display_question_interface(current_case, task_type)
    
    # 提交和导航按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # 上一题按钮
        total_cases = len(st.session_state.data_loader.data.get('cases', []))
        if st.session_state.current_case_index > 0:
            if st.button("⬅️ 上一题", use_container_width=True):
                st.session_state.current_case_index -= 1
                st.session_state.user_answers = {}
                st.session_state.question_started = False
                st.session_state.answer_submitted = False
                st.session_state.start_time = None
                st.rerun()
        else:
            st.button("⬅️ 上一题", disabled=True, use_container_width=True)
    
    with col2:
        if st.button("✅ 提交答案", type="primary", use_container_width=True):
            submit_answer(current_case)
    
    with col3:
        # 下一题按钮
        if st.session_state.current_case_index < total_cases - 1:
            if st.button("➡️ 下一题", use_container_width=True):
                st.session_state.current_case_index += 1
                st.session_state.user_answers = {}
                st.session_state.question_started = False
                st.session_state.answer_submitted = False
                st.session_state.start_time = None
                st.rerun()
        else:
            st.button("➡️ 下一题", disabled=True, use_container_width=True)
    
    # 显示答题时间
    if st.session_state.start_time:
        elapsed_time = time.time() - st.session_state.start_time
        st.info(f"⏱️ 答题时间: {elapsed_time:.1f} 秒")

def display_question_interface(case, task_type):
    """根据任务类型显示不同的答题界面"""
    
    # 根据任务类型显示不同的界面
    if task_type in ["NextSpotForecasting", "MultiTrajectoryForecasting"]:
        # 选择+时间范围填空任务
        display_option_and_time_fields(case)
    elif task_type == "TrajectoryForecasting":
        # 轨迹预测任务（只有轨迹预测填空）
        display_trajectory_forecasting_fields(case)
    else:
        # 纯选择题任务
        display_option_only_fields(case)

def display_option_only_fields(case):
    """显示纯选择题界面"""
    choices = case.get('choices', [])
    if choices:
        st.markdown('<h4>🔘 选项</h4>', unsafe_allow_html=True)
        
        # 单选
        selected_option = st.radio(
            "Choose the correct answer:",
            choices,
            index=st.session_state.user_answers.get('option_index', 0)
        )
        st.session_state.user_answers['option_index'] = choices.index(selected_option) if selected_option in choices else 0
        st.session_state.user_answers['options'] = [selected_option]

def display_option_and_time_fields(case):
    """显示选项+时间范围填空界面"""
    choices = case.get('choices', [])
    if choices:
        st.markdown('<h4>🔘 选项</h4>', unsafe_allow_html=True)
        
        # 单选
        selected_option = st.radio(
            "Choose the correct answer:",
            choices,
            index=st.session_state.user_answers.get('option_index', 0)
        )
        st.session_state.user_answers['option_index'] = choices.index(selected_option) if selected_option in choices else 0
        st.session_state.user_answers['options'] = [selected_option]
    
    # 显示时间范围填空
    display_time_range_fields(case)

def display_time_range_fields(case):
    """显示时间范围填空题"""
    st.markdown('<h4>⏰ 时间范围填空</h4>', unsafe_allow_html=True)
    
    # 检查是否有时间信息
    time_fields = []
    
    # 检查correct_time_str字段
    if 'correct_time_str' in case and case['correct_time_str']:
        for i, time_str in enumerate(case['correct_time_str']):
            if '-' in time_str:
                start_time, end_time = time_str.split('-')
                time_fields.append((f'time_range_{i}_start', f'时间范围 {i+1} 开始时间', start_time))
                time_fields.append((f'time_range_{i}_end', f'时间范围 {i+1} 结束时间', end_time))
            else:
                time_fields.append((f'time_range_{i}', f'时间范围 {i+1}', time_str))
    
    # 检查start_point和end_point字段
    if 'start_point' in case and case['start_point'].get('time'):
        time_fields.append(('start_time', '开始时间', case['start_point']['time']))
    if 'end_point' in case and case['end_point'].get('time'):
        time_fields.append(('end_time', '结束时间', case['end_point']['time']))
    
    if time_fields:
        time_answers = {}
        
        for field_id, field_name, gt_time in time_fields:
            time_input = st.text_input(
                f"{field_name} (格式: HH:MM:SS.mmm)",
                value=st.session_state.user_answers.get(field_id, ''),
                help=f"正确答案格式: {gt_time}"
            )
            # 自动纠正时间格式（将冒号改为点号）
            if time_input and time_input.count(':') > 2:
                # 如果冒号超过2个，将最后一个冒号改为点号
                parts = time_input.split(':')
                if len(parts) > 3:
                    time_input = ':'.join(parts[:-1]) + '.' + parts[-1]
            time_answers[field_id] = time_input
        
        st.session_state.user_answers.update(time_answers)
    else:
        st.info("该题目没有时间范围填空要求")

def display_trajectory_forecasting_fields(case):
    """显示轨迹预测填空题"""
    st.markdown('<h4>🎯 轨迹预测</h4>', unsafe_allow_html=True)
    
    # 获取选项和正确答案
    choices = case.get('choices', [])
    correct_cam_names = case.get('correct_cam_name', [])
    correct_time_strs = case.get('correct_time_str', [])
    
    # 第一段预测
    st.markdown("**第一段预测:**")
    
    # 第一个摄像头选择
    if choices:
        first_camera_option = st.radio(
            "第一个摄像头:",
            choices,
            index=st.session_state.user_answers.get('first_camera_index', 0),
            key="first_camera_radio"
        )
        first_camera_index = choices.index(first_camera_option) if first_camera_option in choices else 0
        first_camera = first_camera_option
    else:
        first_camera = st.text_input(
            "第一个摄像头ID:",
            value=st.session_state.user_answers.get('first_camera', ''),
            help=f"正确答案: {correct_cam_names[0] if len(correct_cam_names) > 0 else '未知'}"
        )
        first_camera_index = 0
    
    # 第一段时间范围
    if len(correct_time_strs) > 0:
        first_time_range = correct_time_strs[0]
        if '-' in first_time_range:
            first_start, first_end = first_time_range.split('-')
        else:
            first_start = first_end = first_time_range
    else:
        first_start = first_end = ""
    
    first_start_time = st.text_input(
        "第一段开始时间 (格式: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('first_start_time', ''),
        help=f"正确答案: {first_start}"
    )
    # 自动纠正时间格式（将冒号改为点号）
    if first_start_time and first_start_time.count(':') > 2:
        # 如果冒号超过2个，将最后一个冒号改为点号
        parts = first_start_time.split(':')
        if len(parts) > 3:
            first_start_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    first_end_time = st.text_input(
        "第一段结束时间 (格式: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('first_end_time', ''),
        help=f"正确答案: {first_end}"
    )
    # 自动纠正时间格式（将冒号改为点号）
    if first_end_time and first_end_time.count(':') > 2:
        # 如果冒号超过2个，将最后一个冒号改为点号
        parts = first_end_time.split(':')
        if len(parts) > 3:
            first_end_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    # 第二段预测
    st.markdown("**第二段预测:**")
    
    # 第二个摄像头选择
    if choices:
        second_camera_option = st.radio(
            "第二个摄像头:",
            choices,
            index=st.session_state.user_answers.get('second_camera_index', 0),
            key="second_camera_radio"
        )
        second_camera_index = choices.index(second_camera_option) if second_camera_option in choices else 0
        second_camera = second_camera_option
    else:
        second_camera = st.text_input(
            "第二个摄像头ID:",
            value=st.session_state.user_answers.get('second_camera', ''),
            help=f"正确答案: {correct_cam_names[1] if len(correct_cam_names) > 1 else '未知'}"
        )
        second_camera_index = 0
    
    # 第二段时间范围
    if len(correct_time_strs) > 1:
        second_time_range = correct_time_strs[1]
        if '-' in second_time_range:
            second_start, second_end = second_time_range.split('-')
        else:
            second_start = second_end = second_time_range
    else:
        second_start = second_end = ""
    
    second_start_time = st.text_input(
        "第二段开始时间 (格式: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('second_start_time', ''),
        help=f"正确答案: {second_start}"
    )
    # 自动纠正时间格式（将冒号改为点号）
    if second_start_time and second_start_time.count(':') > 2:
        # 如果冒号超过2个，将最后一个冒号改为点号
        parts = second_start_time.split(':')
        if len(parts) > 3:
            second_start_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    second_end_time = st.text_input(
        "第二段结束时间 (格式: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('second_end_time', ''),
        help=f"正确答案: {second_end}"
    )
    # 自动纠正时间格式（将冒号改为点号）
    if second_end_time and second_end_time.count(':') > 2:
        # 如果冒号超过2个，将最后一个冒号改为点号
        parts = second_end_time.split(':')
        if len(parts) > 3:
            second_end_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    # 保存答案
    st.session_state.user_answers.update({
        'first_camera': first_camera,
        'first_camera_index': first_camera_index,
        'first_start_time': first_start_time,
        'first_end_time': first_end_time,
        'second_camera': second_camera,
        'second_camera_index': second_camera_index,
        'second_start_time': second_start_time,
        'second_end_time': second_end_time
    })

def submit_answer(current_case):
    """提交答案并计算得分"""
    end_time = time.time()
    elapsed_time = end_time - st.session_state.start_time
    
    # 计算得分
    score_result = st.session_state.scoring_system.calculate_score_new(
        current_case,
        st.session_state.user_answers,
        elapsed_time
    )
    
    # 保存结果
    result = {
        'case_id': current_case.get('case_id', ''),
        'task_type': st.session_state.current_task if st.session_state.current_task else '',
        'user_answers': st.session_state.user_answers.copy(),
        'ground_truth': current_case.get('correct_cam_name', current_case.get('ground_truth', '')),
        'score': score_result['score'],
        'time_score': score_result['time_score'],
        'accuracy_score': score_result['accuracy_score'],
        'elapsed_time': elapsed_time,
        'timestamp': datetime.now().isoformat()
    }
    
    st.session_state.results.append(result)
    
    # 显示结果
    show_result(result, current_case)
    
    # 设置答案已提交状态
    st.session_state.answer_submitted = True

def show_result(result, current_case):
    """显示答题结果"""
    st.markdown('<h3 class="sub-header">📊 答题结果</h3>', unsafe_allow_html=True)
    
    if result['accuracy_score'] > 0:
        st.markdown('<div class="result-correct">✅ 回答正确！</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-incorrect">❌ 回答错误</div>', unsafe_allow_html=True)
    
    # 显示详细信息
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("总得分", f"{result['score']:.2f}")
        st.metric("准确率得分", f"{result['accuracy_score']:.2f}")
        st.metric("时间得分", f"{result['time_score']:.2f}")
    
    with col2:
        st.metric("答题时间", f"{result['elapsed_time']:.1f}秒")
        st.metric("题目类型", result['task_type'])
        st.metric("题目ID", result['case_id'])
    
    # 显示正确答案
    st.markdown('<h4>📋 正确答案</h4>', unsafe_allow_html=True)
    
    # 直接显示correct_cam_name和correct_time_str字段
    correct_cam_names = current_case.get('correct_cam_name', [])
    correct_time_strs = current_case.get('correct_time_str', [])
    
    if correct_cam_names:
        st.info(f"**correct_cam_name:** {correct_cam_names}")
    
    if correct_time_strs:
        st.info(f"**correct_time_str:** {correct_time_strs}")
    
    # 如果没有这些字段，显示ground_truth
    if not correct_cam_names and not correct_time_strs:
        ground_truth = current_case.get('ground_truth', '')
        st.info(f"**ground_truth:** {ground_truth}")
    
    # 显示用户答案
    st.markdown('<h4>👤 您的答案</h4>', unsafe_allow_html=True)
    user_answers = result['user_answers']
    
    if 'options' in user_answers:
        st.write(f"**选项答案:** {', '.join(user_answers['options'])}")
    
    time_answers = {k: v for k, v in user_answers.items() if k.endswith('_time')}
    if time_answers:
        st.write("**时间答案:**")
        for field, answer in time_answers.items():
            st.write(f"- {field}: {answer}")
    
    # 显示轨迹预测答案
    trajectory_fields = ['first_camera', 'first_start_time', 'first_end_time', 
                        'second_camera', 'second_start_time', 'second_end_time']
    trajectory_answers = {k: v for k, v in user_answers.items() if k in trajectory_fields}
    if trajectory_answers:
        st.write("**轨迹预测答案:**")
        
        # 第一段
        first_camera = trajectory_answers.get('first_camera', '')
        first_start = trajectory_answers.get('first_start_time', '')
        first_end = trajectory_answers.get('first_end_time', '')
        if first_camera:
            st.write(f"📹 **第一个摄像头ID:** {first_camera}")
            if first_start and first_end:
                st.write(f"⏰ **第一段时间范围:** {first_start} - {first_end}")
            elif first_start:
                st.write(f"⏰ **第一段时间:** {first_start}")
        
        # 第二段
        second_camera = trajectory_answers.get('second_camera', '')
        second_start = trajectory_answers.get('second_start_time', '')
        second_end = trajectory_answers.get('second_end_time', '')
        if second_camera:
            st.write(f"📹 **第二个摄像头ID:** {second_camera}")
            if second_start and second_end:
                st.write(f"⏰ **第二段时间范围:** {second_start} - {second_end}")
            elif second_start:
                st.write(f"⏰ **第二段时间:** {second_start}")

def show_results_summary():
    """显示答题结果汇总"""
    if not st.session_state.results:
        st.warning("暂无答题记录")
        return
    
    st.markdown('<h3 class="sub-header">📈 答题结果汇总</h3>', unsafe_allow_html=True)
    
    # 创建结果DataFrame
    df = pd.DataFrame(st.session_state.results)
    
    # 显示统计信息
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总题目数", len(df))
    
    with col2:
        correct_count = len(df[df['accuracy_score'] > 0])
        st.metric("正确题目数", correct_count)
    
    with col3:
        accuracy = correct_count / len(df) * 100 if len(df) > 0 else 0
        st.metric("正确率", f"{accuracy:.1f}%")
    
    with col4:
        avg_score = df['score'].mean() if len(df) > 0 else 0
        st.metric("平均得分", f"{avg_score:.2f}")
    
    # 显示详细结果表格
    st.markdown('<h4>📋 详细结果</h4>', unsafe_allow_html=True)
    
    # 简化显示列
    display_df = df[['case_id', 'task_type', 'score', 'accuracy_score', 'time_score', 'elapsed_time']].copy()
    display_df['elapsed_time'] = display_df['elapsed_time'].round(1)
    display_df['score'] = display_df['score'].round(2)
    display_df['accuracy_score'] = display_df['accuracy_score'].round(2)
    display_df['time_score'] = display_df['time_score'].round(2)
    
    st.dataframe(display_df, use_container_width=True)
    
    # 导出结果
    if st.button("📥 导出结果"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="下载CSV文件",
            data=csv,
            file_name=f"答题结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


def display_results_visualization():
    """显示结果可视化界面"""
    st.markdown('<h2 class="sub-header">📊 评估结果可视化</h2>', unsafe_allow_html=True)
    
    # 初始化session state
    if 'results_data' not in st.session_state:
        st.session_state.results_data = {}
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = None
    if 'selected_scene' not in st.session_state:
        st.session_state.selected_scene = None
    if 'selected_task' not in st.session_state:
        st.session_state.selected_task = None
    
    # 结果文件选择
    st.markdown('<h3>📁 选择结果文件</h3>', unsafe_allow_html=True)
    
    # 查找结果文件
    result_files = []
    eval_dir = "./eval/results"
    if os.path.exists(eval_dir):
        for file in os.listdir(eval_dir):
            if file.endswith('.json') and not file.startswith('prompt_'):
                result_files.append(file)
    
    if not result_files:
        st.warning("未找到评估结果文件，请先运行评估脚本")
        if st.button("🔙 返回主界面"):
            st.session_state.show_results = False
            st.rerun()
        return
    
    # 结果文件选择
    selected_file = st.selectbox("选择评估结果文件", result_files, index=0)
    
    if selected_file != st.session_state.get('selected_file'):
        st.session_state.selected_file = selected_file
        st.session_state.results_data = {}
        st.rerun()
    
    # 加载选中的结果文件
    if st.session_state.selected_file and st.session_state.selected_file not in st.session_state.results_data:
        file_path = os.path.join(eval_dir, st.session_state.selected_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            st.session_state.results_data[st.session_state.selected_file] = data
            st.success(f"✅ 已加载评估结果文件: {st.session_state.selected_file}")
        except Exception as e:
            st.error(f"❌ 加载结果文件失败: {str(e)}")
            return
    
    # 显示结果统计
    if st.session_state.selected_file in st.session_state.results_data:
        results = st.session_state.results_data[st.session_state.selected_file]
        # 从文件名中提取模型名称用于显示
        model_name = st.session_state.selected_file.split('_')[0] + '_' + st.session_state.selected_file.split('_')[1] if '_' in st.session_state.selected_file else st.session_state.selected_file.split('_')[0]
        display_results_statistics(results, model_name)
        
        # 场景和任务类型过滤
        st.markdown('<h3>🔍 结果筛选</h3>', unsafe_allow_html=True)
        
        # 获取所有场景和任务类型
        scenes = list(set([r.get('scene', 'unknown') for r in results]))
        task_types = list(set([r.get('task_id', 'unknown') for r in results]))  # 使用task_id字段
        
        col1, col2 = st.columns(2)
        with col1:
            selected_scene = st.selectbox("选择场景", ["全部"] + scenes, index=0)
        with col2:
            selected_task = st.selectbox("选择任务类型", ["全部"] + task_types, index=0)
        
        # 过滤结果
        filtered_results = results
        if selected_scene != "全部":
            filtered_results = [r for r in filtered_results if r.get('scene') == selected_scene]
        if selected_task != "全部":
            filtered_results = [r for r in filtered_results if r.get('task_id') == selected_task]  # 使用task_id字段
        
        # 显示详细结果
        if filtered_results:
            display_detailed_results(filtered_results, selected_scene, selected_task)
        else:
            st.info("没有符合条件的结果")
    
    # 返回按钮
    if st.button("🔙 返回主界面"):
        st.session_state.show_results = False
        st.rerun()

def display_results_statistics(results, model_name):
    """显示结果统计信息"""
    st.markdown('<h3>📈 总体统计</h3>', unsafe_allow_html=True)
    
    total_cases = len(results)
    correct_cases = sum(1 for r in results if r.get('metrics', {}).get('MCQacc', 0) > 0)
    avg_score = sum(r.get('metrics', {}).get('score', 0) for r in results) / total_cases if total_cases > 0 else 0
    avg_mcq = sum(r.get('metrics', {}).get('MCQacc', 0) for r in results) / total_cases if total_cases > 0 else 0
    avg_time_iou = sum(r.get('metrics', {}).get('TimeIoU', 0) for r in results) / total_cases if total_cases > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("模型", model_name)
    with col2:
        st.metric("总题目数", total_cases)
    with col3:
        st.metric("正确题目数", correct_cases)
    with col4:
        st.metric("平均得分", f"{avg_score:.3f}")
    with col5:
        st.metric("平均MCQ", f"{avg_mcq:.3f}")
    
    # 按场景统计
    st.markdown('<h4>📊 按场景统计</h4>', unsafe_allow_html=True)
    scene_stats = {}
    for result in results:
        scene = result.get('scene', 'unknown')
        if scene not in scene_stats:
            scene_stats[scene] = {'total': 0, 'correct': 0, 'scores': [], 'mcqs': []}
        
        scene_stats[scene]['total'] += 1
        if result.get('metrics', {}).get('MCQacc', 0) > 0:
            scene_stats[scene]['correct'] += 1
        scene_stats[scene]['scores'].append(result.get('metrics', {}).get('score', 0))
        scene_stats[scene]['mcqs'].append(result.get('metrics', {}).get('MCQacc', 0))
    
    scene_df = pd.DataFrame([
        {
            '场景': scene,
            '题目数': stats['total'],
            '正确数': stats['correct'],
            '正确率': f"{stats['correct']/stats['total']*100:.1f}%" if stats['total'] > 0 else "0%",
            '平均得分': f"{sum(stats['scores'])/len(stats['scores']):.3f}" if stats['scores'] else "0.000",
            '平均MCQ': f"{sum(stats['mcqs'])/len(stats['mcqs']):.3f}" if stats['mcqs'] else "0.000"
        }
        for scene, stats in scene_stats.items()
    ])
    
    st.dataframe(scene_df, use_container_width=True)
    
    # 按任务类型统计
    st.markdown('<h4>📊 按任务类型统计</h4>', unsafe_allow_html=True)
    task_stats = {}
    for result in results:
        task = result.get('task_id', 'unknown')  # 使用task_id字段
        if task not in task_stats:
            task_stats[task] = {'total': 0, 'correct': 0, 'scores': [], 'mcqs': []}
        
        task_stats[task]['total'] += 1
        if result.get('metrics', {}).get('MCQacc', 0) > 0:
            task_stats[task]['correct'] += 1
        task_stats[task]['scores'].append(result.get('metrics', {}).get('score', 0))
        task_stats[task]['mcqs'].append(result.get('metrics', {}).get('MCQacc', 0))
    
    task_df = pd.DataFrame([
        {
            '任务类型': task,
            '题目数': stats['total'],
            '正确数': stats['correct'],
            '正确率': f"{stats['correct']/stats['total']*100:.1f}%" if stats['total'] > 0 else "0%",
            '平均得分': f"{sum(stats['scores'])/len(stats['scores']):.3f}" if stats['scores'] else "0.000",
            '平均MCQ': f"{sum(stats['mcqs'])/len(stats['mcqs']):.3f}" if stats['mcqs'] else "0.000"
        }
        for task, stats in task_stats.items()
    ])
    
    st.dataframe(task_df, use_container_width=True)

def display_detailed_results(results, scene_filter, task_filter):
    """显示详细结果"""
    st.markdown('<h3>📋 详细结果</h3>', unsafe_allow_html=True)
    
    # 创建结果表格
    display_data = []
    for result in results:
        # 获取ground_truth
        ground_truth = result.get('response', {}).get('ground_truth', {})
        if isinstance(ground_truth, dict):
            ground_truth_str = str(ground_truth)
        else:
            ground_truth_str = str(ground_truth)
        
        display_data.append({
            'Case ID': result.get('case_id', ''),
            '场景': result.get('scene', ''),
            '任务类型': result.get('task_id', ''),  # 使用task_id字段
            '得分': f"{result.get('metrics', {}).get('score', 0):.3f}",
            'MCQ': f"{result.get('metrics', {}).get('MCQacc', 0):.3f}",
            'TimeIoU': f"{result.get('metrics', {}).get('TimeIoU', 0):.3f}",
            '模型答案': result.get('response', {}).get('model_answer', '')[:100] + '...' if len(result.get('response', {}).get('model_answer', '')) > 100 else result.get('response', {}).get('model_answer', ''),
            '提取答案': str(result.get('response', {}).get('answer', [])),
            '时间范围': str(result.get('response', {}).get('time_duration', [])),
            '正确答案': ground_truth_str[:100] + '...' if len(ground_truth_str) > 100 else ground_truth_str
        })
    
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True)
    
    # 添加题目详情查看功能
    st.markdown('<h4>🔍 查看题目详情</h4>', unsafe_allow_html=True)
    
    # 选择要查看的案例
    case_ids = [result.get('case_id', '') for result in results]
    selected_case_id = st.selectbox("选择Case ID查看详情", case_ids, index=0)
    
    if selected_case_id:
        # 从结果中找到选中的案例
        selected_result = next((r for r in results if r.get('case_id') == selected_case_id), None)
        if selected_result:
            display_case_details(selected_result)
    
    # 导出功能
    if st.button("📥 导出结果"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="下载CSV文件",
            data=csv,
            file_name=f"评估结果_{scene_filter}_{task_filter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def display_case_details(result):
    """显示单个案例的详细信息"""
    case_id = result.get('case_id', '')
    scene = result.get('scene', '')
    task_type = result.get('task_id', '')  # 使用task_id字段
    
    st.markdown(f'<h5>📝 案例详情: {case_id}</h5>', unsafe_allow_html=True)
    
    # 尝试从原始数据中加载题目详情
    try:
        # 构建数据文件路径
        data_file = f"data/{scene}/{scene}_{task_type}_30.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 查找对应的案例
            case_data = None
            for case in data.get('cases', []):
                if case.get('case_id') == case_id:
                    case_data = case
                    break
            
            if case_data:
                # 显示题目内容
                st.markdown('<h6>📋 题目内容</h6>', unsafe_allow_html=True)
                st.write(case_data.get('question', ''))
                
                # 显示选项
                choices = case_data.get('choices', [])
                if choices:
                    st.markdown('<h6>🔘 选项</h6>', unsafe_allow_html=True)
                    for i, choice in enumerate(choices):
                        st.write(f"{chr(65+i)}. {choice}")
                
                # 显示地图图像
                if case_data.get('map_image_path'):
                    st.markdown('<h6>🗺️ 场景地图</h6>', unsafe_allow_html=True)
                    map_path = case_data['map_image_path']
                    if map_path.startswith('./'):
                        map_path = os.path.join(
                            os.getcwd(),
                            map_path.replace('./', '')
                        )
                    
                    if os.path.exists(map_path):
                        try:
                            map_image = Image.open(map_path)
                            st.image(map_image, use_container_width=True)
                        except Exception as e:
                            st.error(f"无法加载地图图像: {str(e)}")
                    else:
                        st.warning(f"地图文件不存在: {map_path}")
                
                # 显示摄像头图像
                camera_images = case_data.get('camera_images', [])
                if camera_images:
                    st.markdown('<h6>📹 摄像头图像</h6>', unsafe_allow_html=True)
                    
                    for i, camera in enumerate(camera_images):
                        camera_id = camera.get('camera_id', f'Camera_{i}')
                        
                        # 对于CausalReordering任务，不显示时间范围
                        if task_type == "CausalReordering":
                            expander_title = f"📹 摄像头 {camera_id}"
                        else:
                            # 转换时间格式
                            start_time_str = seconds_to_time_format(camera['start_timestamp'])
                            end_time_str = seconds_to_time_format(camera['end_timestamp'])
                            expander_title = f"📹 摄像头 {camera_id} (时间: {start_time_str} - {end_time_str})"
                        
                        with st.expander(expander_title):
                            # 显示视频路径信息
                            video_path = camera.get('video_path', '')
                            
                            # 处理相对路径，转换为绝对路径
                            if video_path.startswith('./'):
                                video_path = os.path.join(
                                    os.getcwd(),
                                    video_path.replace('./', '')
                                )
                            
                            st.write(f"**视频路径:** {video_path}")
                            
                            # 检查视频文件是否存在
                            if os.path.exists(video_path):
                                st.success("✅ 视频文件存在")
                                
                                # 从视频中提取帧
                                frames = st.session_state.video_processor.extract_frames(
                                    video_path,
                                    camera['frame_ids'],
                                    camera['bboxes']
                                )
                                
                                if frames:
                                    # 显示3张均匀选择的帧
                                    cols = st.columns(3)
                                    for j, frame in enumerate(frames):
                                        with cols[j]:
                                            st.image(frame, caption=f"帧 {camera['frame_ids'][j]}", use_container_width=True)
                                else:
                                    st.warning(f"无法从视频中提取帧")
                            else:
                                st.error(f"❌ 视频文件不存在: {video_path}")
            else:
                st.warning(f"未找到案例 {case_id} 的原始数据")
        else:
            st.warning(f"数据文件不存在: {data_file}")
    except Exception as e:
        st.error(f"加载题目详情时出错: {str(e)}")
    
    # 显示评估结果
    st.markdown('<h6>📊 评估结果</h6>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("得分", f"{result.get('metrics', {}).get('score', 0):.3f}")
    with col2:
        st.metric("MCQ", f"{result.get('metrics', {}).get('MCQacc', 0):.3f}")
    with col3:
        st.metric("TimeIoU", f"{result.get('metrics', {}).get('TimeIoU', 0):.3f}")
    
    # 显示模型回答
    st.markdown('<h6>🤖 模型回答</h6>', unsafe_allow_html=True)
    model_answer = result.get('response', {}).get('model_answer', '')
    st.text_area("模型原始回答", model_answer, height=200, disabled=True)
    
    # 显示提取的答案
    st.markdown('<h6>📝 提取的答案</h6>', unsafe_allow_html=True)
    extracted_answer = result.get('response', {}).get('answer', [])
    time_duration = result.get('response', {}).get('time_duration', [])
    
    st.write(f"**选择题答案**: {extracted_answer}")
    st.write(f"**时间范围**: {time_duration}")
    
    # 显示正确答案
    st.markdown('<h6>✅ 正确答案</h6>', unsafe_allow_html=True)
    ground_truth = result.get('response', {}).get('ground_truth', {})
    st.write(f"**Ground Truth**: {ground_truth}")

def display_eval_interface():
    """显示模型评估界面"""
    st.markdown('<h2 class="sub-header">🤖 模型评估系统</h2>', unsafe_allow_html=True)
    
    # 返回按钮
    if st.button("🔙 返回主界面"):
        st.session_state.show_eval = False
        st.rerun()
    
    # 评估配置
    st.markdown('<h3>⚙️ 评估配置</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 模型配置
        st.markdown('<h4>🔧 模型配置</h4>', unsafe_allow_html=True)
        model_name = st.text_input("模型名称", help="例如: claude-sonnet-4-20250514-thinking, gpt-4o")
        api_key = st.text_input("API Key", type="password", help="OpenAI API密钥")
        base_url = st.text_input("Base URL", help="API基础URL")
        
        # 模型参数
        st.markdown('<h4>🎛️ 模型参数</h4>', unsafe_allow_html=True)
        max_tokens = st.number_input("Max Tokens", min_value=1, max_value=32768, value=16384)
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.1, step=0.1)
    
    with col2:
        # 测试配置
        st.markdown('<h4>📋 测试配置</h4>', unsafe_allow_html=True)
        
        # 测试范围选择
        test_scope = st.radio(
            "测试范围",
            ["特定场景-任务", "全部场景-任务"],
            help="选择特定场景任务或全部场景任务"
        )
        
        if test_scope == "特定场景-任务":
            # 特定场景任务选择
            scene = st.selectbox("场景", ["indoor", "outdoor"])
            task_type = st.selectbox(
                "任务类型",
                ["MotionState", "GeoLocation", "ArrivalTimeInterval", "CausalReordering", 
                 "TrajectoryForecasting", "NextSpotForecasting", "MultiTargetTrajectoryForecasting"]
            )
            max_cases = st.number_input("测试案例数", min_value=1, max_value=30, value=5)
            
            # 计算总案例数
            total_cases = max_cases
            
        else:
            # 全部场景任务
            max_cases_per_scene = st.number_input("每个场景测试案例数", min_value=1, max_value=30, value=5)
            
            # 计算总案例数 (2个场景 × 7个任务类型 × 每个场景案例数)
            total_cases = 2 * 7 * max_cases_per_scene
    
    # 显示预估信息
    st.info(f"📊 预估总测试案例数: {total_cases}")
    
    # 开始评估和停止评估按钮
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 开始评估", type="primary", use_container_width=True):
            if not model_name or not api_key or not base_url:
                st.error("❌ 请填写完整的模型配置信息")
            else:
                start_evaluation(model_name, api_key, base_url, max_tokens, temperature, 
                               test_scope, scene if test_scope == "特定场景-任务" else None,
                               task_type if test_scope == "特定场景-任务" else None,
                               max_cases if test_scope == "特定场景-任务" else max_cases_per_scene)
    
    with col2:
        if st.button("⏹️ 停止评估", use_container_width=True):
            stop_evaluation()
    
    # 显示评估进度
    if st.session_state.eval_status == "running":
        display_eval_progress()
    elif st.session_state.eval_status == "completed":
        display_eval_completion()
    elif st.session_state.eval_status == "error":
        display_eval_error()

def start_evaluation(model_name, api_key, base_url, max_tokens, temperature, test_scope, scene, task_type, max_cases):
    """开始评估"""
    st.session_state.eval_status = "running"
    st.session_state.eval_progress = 0
    st.session_state.eval_total = 0
    st.session_state.eval_output = []
    
    # 构建eval.py命令
    cmd = [
        "python", "eval/eval.py",
        "--model", model_name,
        "--api-key", api_key,
        "--base-url", base_url,
        "--data-dir", "data",
        "--result-dir", "eval/results",
        "--max-cases", str(max_cases),
        "--max-tokens", str(max_tokens),
        "--temperature", str(temperature),
        "--verbose"
    ]
    
    if test_scope == "特定场景-任务":
        cmd.extend(["--scene", scene, "--task-type", task_type])
    
    # 使用队列在线程间传递数据
    output_queue = queue.Queue()
    status_queue = queue.Queue()
    
    # 在后台线程中运行评估
    def run_eval():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # 读取输出
            for line in iter(process.stdout.readline, ''):
                if line:
                    output_queue.put(line.strip())
                    
                    # 解析进度信息
                    if "Processing case" in line:
                        # 提取当前进度
                        try:
                            parts = line.split("Processing case ")[1].split("/")
                            current = int(parts[0])
                            total = int(parts[1].split(":")[0])
                            status_queue.put(("progress", current, total))
                        except:
                            pass
            
            # 等待进程完成
            return_code = process.wait()
            
            if return_code == 0:
                status_queue.put(("status", "completed"))
            else:
                status_queue.put(("status", "error"))
                
        except Exception as e:
            output_queue.put(f"Error: {str(e)}")
            status_queue.put(("status", "error"))
    
    # 启动后台线程
    thread = threading.Thread(target=run_eval)
    thread.daemon = True
    thread.start()
    
    # 将队列存储到session_state中
    st.session_state.eval_output_queue = output_queue
    st.session_state.eval_status_queue = status_queue
    
    st.success("✅ 评估已开始，请查看下方进度信息")

def stop_evaluation():
    """停止评估"""
    if 'eval_process' in st.session_state and st.session_state.eval_process:
        try:
            st.session_state.eval_process.terminate()
            st.session_state.eval_status = "stopped"
            st.success("⏹️ 评估已停止")
        except Exception as e:
            st.error(f"停止评估时出错: {str(e)}")
    else:
        st.warning("没有正在运行的评估进程")

def display_eval_progress():
    """显示评估进度"""
    st.markdown('<h3>📊 评估进度</h3>', unsafe_allow_html=True)
    
    # 处理队列中的数据
    if 'eval_output_queue' in st.session_state:
        output_queue = st.session_state.eval_output_queue
        while not output_queue.empty():
            try:
                line = output_queue.get_nowait()
                st.session_state.eval_output.append(line)
            except queue.Empty:
                break
    
    if 'eval_status_queue' in st.session_state:
        status_queue = st.session_state.eval_status_queue
        while not status_queue.empty():
            try:
                status_data = status_queue.get_nowait()
                if status_data[0] == "progress":
                    st.session_state.eval_progress = status_data[1]
                    st.session_state.eval_total = status_data[2]
                elif status_data[0] == "status":
                    st.session_state.eval_status = status_data[1]
            except queue.Empty:
                break
    
    # 进度条
    if st.session_state.eval_total > 0:
        progress = st.session_state.eval_progress / st.session_state.eval_total
        st.progress(progress)
        st.write(f"进度: {st.session_state.eval_progress}/{st.session_state.eval_total} ({progress*100:.1f}%)")
    else:
        st.progress(0)
        st.write("正在初始化...")
    
    # 显示prompt文件路径
    st.markdown('<h4>📁 Prompt文件路径</h4>', unsafe_allow_html=True)
    
    # 从输出中提取prompt文件路径
    prompt_files = []
    if st.session_state.eval_output:
        for line in st.session_state.eval_output:
            if "完整对话记录已导出到:" in line:
                file_path = line.split("完整对话记录已导出到: ")[1]
                prompt_files.append(file_path)
    
    if prompt_files:
        # 显示最新的几个prompt文件路径
        recent_files = prompt_files[-5:]  # 显示最近5个文件
        for file_path in recent_files:
            st.text(f"📄 {file_path}")
    else:
        st.info("暂无prompt文件生成")
    
    # 自动刷新
    time.sleep(1)
    st.rerun()

def display_eval_completion():
    """显示评估完成"""
    st.markdown('<h3>✅ 评估完成</h3>', unsafe_allow_html=True)
    
    # 显示最终输出
    st.markdown('<h4>📝 最终输出</h4>', unsafe_allow_html=True)
    
    if st.session_state.eval_output:
        # 显示所有输出
        for line in st.session_state.eval_output:
            if "Error" in line or "Failed" in line:
                st.error(line)
            elif "Completed" in line or "Success" in line:
                st.success(line)
            elif "Processing case" in line:
                st.info(line)
            else:
                st.text(line)
    
    # 重置状态按钮
    if st.button("🔄 重新开始评估"):
        st.session_state.eval_status = "idle"
        st.session_state.eval_output = []
        st.session_state.eval_progress = 0
        st.session_state.eval_total = 0
        # 清理队列
        if 'eval_output_queue' in st.session_state:
            del st.session_state.eval_output_queue
        if 'eval_status_queue' in st.session_state:
            del st.session_state.eval_status_queue
        st.rerun()
    
    # 查看结果按钮
    if st.button("📈 查看评估结果"):
        st.session_state.show_eval = False
        st.session_state.show_results = True
        st.rerun()

def display_eval_error():
    """显示评估错误"""
    st.markdown('<h3>❌ 评估出错</h3>', unsafe_allow_html=True)
    
    # 显示错误输出
    st.markdown('<h4>📝 错误信息</h4>', unsafe_allow_html=True)
    
    if st.session_state.eval_output:
        for line in st.session_state.eval_output:
            st.error(line)
    
    # 重置状态按钮
    if st.button("🔄 重新开始评估"):
        st.session_state.eval_status = "idle"
        st.session_state.eval_output = []
        st.session_state.eval_progress = 0
        st.session_state.eval_total = 0
        # 清理队列
        if 'eval_output_queue' in st.session_state:
            del st.session_state.eval_output_queue
        if 'eval_status_queue' in st.session_state:
            del st.session_state.eval_status_queue
        st.rerun()

def display_ground_truth(case, task_type):
    """根据任务类型显示正确的GT信息"""
    
    # 处理任务类型，确保使用正确的格式
    if task_type == "Next Spot Forecasting":
        task_type = "NextSpotForecasting"
    elif task_type == "Trajectory Forecasting":
        task_type = "TrajectoryForecasting"
    elif task_type == "Multi Trajectory Forecasting" or task_type == "Multi-Target Trajectory Forecasting":
        task_type = "MultiTrajectoryForecasting"
    elif ' ' in task_type:
        task_type = task_type.split()[-1]
    
    # 纯选择题任务：只显示选项答案
    if task_type in ["MotionState", "GeoLocation", "ArrivalTimeInterval", "CausalReordering"]:
        # 尝试从correct_cam_name获取，如果没有则从ground_truth获取
        correct_cam_names = case.get('correct_cam_name', [])
        if correct_cam_names:
            st.info(f"**正确答案:** {correct_cam_names[0]}")
        else:
            ground_truth = case.get('ground_truth', '')
            st.info(f"**正确答案:** {ground_truth}")
    
    # 选择+填空任务：显示camera选择和时间范围
    elif task_type in ["NextSpotForecasting", "MultiTrajectoryForecasting"]:
        correct_cam_names = case.get('correct_cam_name', [])
        correct_time_strs = case.get('correct_time_str', [])
        
        if correct_cam_names:
            st.info(f"**摄像头答案:** {correct_cam_names[0]}")
        
        if correct_time_strs:
            for i, time_str in enumerate(correct_time_strs):
                if '-' in time_str:
                    start_time, end_time = time_str.split('-')
                    st.info(f"**时间范围 {i+1}:** {start_time} - {end_time}")
                else:
                    st.info(f"**时间点 {i+1}:** {time_str}")
    
    # 轨迹预测任务：显示两个camera和两个时间范围
    elif task_type == "TrajectoryForecasting":
        correct_cam_names = case.get('correct_cam_name', [])
        correct_time_strs = case.get('correct_time_str', [])
        
        if correct_cam_names and len(correct_cam_names) >= 2:
            st.info(f"**第一段摄像头:** {correct_cam_names[0]}")
            st.info(f"**第二段摄像头:** {correct_cam_names[1]}")
        
        if correct_time_strs and len(correct_time_strs) >= 2:
            # 第一段时间
            first_time = correct_time_strs[0]
            if '-' in first_time:
                start_time, end_time = first_time.split('-')
                st.info(f"**第一段时间范围:** {start_time} - {end_time}")
            else:
                st.info(f"**第一段时间点:** {first_time}")
            
            # 第二段时间
            second_time = correct_time_strs[1]
            if '-' in second_time:
                start_time, end_time = second_time.split('-')
                st.info(f"**第二段时间范围:** {start_time} - {end_time}")
            else:
                st.info(f"**第二段时间点:** {second_time}")
    
    else:
        # 默认情况
        ground_truth = case.get('ground_truth', '')
        st.info(f"**正确答案:** {ground_truth}")

if __name__ == "__main__":
    main()
