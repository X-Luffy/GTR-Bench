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
    Convert seconds to 12:00:00.000 format
    
    Args:
        seconds: Number of seconds (float)
        
    Returns:
        Formatted time string
    """
    # Calculate hours, minutes, seconds and milliseconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    
    # Format as 12:00:00.000
    return f"12:{minutes:02d}:{secs:02d}.{milliseconds:03d}"

# Set page configuration
st.set_page_config(
    page_title="Human-Level Evaluation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styles
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
    # Initialize session state
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
    
    # Evaluation function related states
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

    # Main title
    st.markdown('<h1 class="main-header">🎯 Human-Level Evaluation System</h1>', unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.markdown('<h3 class="sub-header">📋 System Configuration</h3>', unsafe_allow_html=True)
        
        # Scene selection
        scene = st.selectbox(
            "Select Scene",
            ["outdoor", "indoor"],
            index=0
        )
        
        # Task type selection
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
            "Select Task Type",
            task_types[scene],
            index=0
        )
        
        # Display task descriptions
        task_descriptions = {
            "MotionState": "Motion State Reasoning - Multiple Choice",
            "GeoLocation": "Geographic Location Reasoning - Multiple Choice", 
            "ArrivalTimeInterval": "Arrival Time Interval Reasoning - Multiple Choice",
            "CausalReordering": "Causal Reordering Reasoning - Multiple Choice",
            "NextSpotForecasting": "Next Spot Forecasting - Multiple Choice + Time Range",
            "TrajectoryForecasting": "Trajectory Forecasting - Predict Two Cameras + Time Range",
            "MultiTargetTrajectoryForecasting": "Multi-Target Trajectory Forecasting - Multiple Choice + Time Range"
        }
        
        if task_type in task_descriptions:
            st.info(f"📝 {task_descriptions[task_type]}")
        
        # Load data
        if st.button("🔄 Load Question Data"):
            try:
                st.session_state.data_loader.load_data(scene, task_type)
                st.session_state.current_task = f"{scene}_{task_type}"
                st.session_state.current_case_index = 0
                st.session_state.user_answers = {}
                st.session_state.question_started = False
                st.session_state.answer_submitted = False
                st.session_state.start_time = None
                # Clear other interface states to ensure return to main interface
                if 'show_results' in st.session_state:
                    del st.session_state.show_results
                if 'show_eval' in st.session_state:
                    del st.session_state.show_eval
                st.success(f"✅ Successfully loaded {scene} - {task_type} question data")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to load data: {str(e)}")
        
        st.markdown("---")
        
        # Display statistics
        if st.session_state.data_loader.data:
            st.markdown('<h4>📊 Statistics</h4>', unsafe_allow_html=True)
            total_cases = len(st.session_state.data_loader.data.get('cases', []))
            st.write(f"Total Questions: {total_cases}")
            st.write(f"Current Question: {st.session_state.current_case_index + 1}")
            
            # Question navigation
            if total_cases > 0:
                case_index = st.slider(
                    "Select Question",
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
        
        # View results
        if st.button("📈 View Answer Results"):
            if st.session_state.results:
                show_results_summary()
            else:
                st.warning("No answer records yet")
        
        st.markdown("---")
        
        # Model evaluation function
        st.markdown('<h4>🤖 Model Evaluation</h4>', unsafe_allow_html=True)
        if st.button("🚀 Launch Model Evaluation"):
            st.session_state.show_eval = True
                st.rerun()
            
        # View evaluation results
        if st.button("📈 View Evaluation Results"):
            st.session_state.show_results = True
                    st.rerun()

    # Main content area
    if 'show_eval' in st.session_state and st.session_state.show_eval:
        # Display model evaluation interface
        display_eval_interface()
    elif 'show_results' in st.session_state and st.session_state.show_results:
        # Display results visualization interface
        display_results_visualization()
    elif st.session_state.data_loader.data and st.session_state.current_task:
        # Display normal question answering interface
            display_current_question()
    else:
        st.info("👈 Please select scene and task type in sidebar, then load question data")

def display_current_question():
    """Display current question"""
    data = st.session_state.data_loader.data
    cases = data.get('cases', [])
    
    if not cases or st.session_state.current_case_index >= len(cases):
        st.error("Question data loading failed or index out of range")
        return
    
    current_case = cases[st.session_state.current_case_index]
    # Extract task type, handle different formats
    task_id = current_case.get('task_id', '')
    if task_id:
        # Use task_id directly as task type
            task_type = task_id
    else:
        task_type = ''
    
    # Initialize answer state
    if 'question_started' not in st.session_state:
        st.session_state.question_started = False
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    
    # Display question information
    st.markdown(f'<h2 class="sub-header">📝 Question {st.session_state.current_case_index + 1}</h2>', unsafe_allow_html=True)
    
    # Display task type information
    task_descriptions = {
        "MotionState": "🎯 Motion State Reasoning Task - Infer target's motion state based on provided video information",
        "GeoLocation": "🎯 Geographic Location Reasoning Task - Infer target's spatial position relationship based on provided video information",
        "ArrivalTimeInterval": "🎯 Arrival Time Interval Reasoning Task - Infer target's temporal sequence based on provided video information",
        "CausalReordering": "🎯 Causal Reordering Reasoning Task - Infer target's causal relationships based on provided video information",
        "NextSpotForecasting": "🎯 Next Spot Forecasting Task - Predict target's next location and time range",
        "TrajectoryForecasting": "🎯 Trajectory Forecasting Task - Predict target's next two locations and corresponding time ranges",
        "MultiTrajectoryForecasting": "🎯 Multi-Trajectory Forecasting Task - Predict multiple targets' trajectories and time ranges"
    }
    
    if task_type in task_descriptions:
        st.markdown(f'<div class="task-info">{task_descriptions[task_type]}</div>', unsafe_allow_html=True)
    
    # Auto start answering (no button needed)
    if not st.session_state.question_started:
                st.session_state.question_started = True
                st.session_state.start_time = time.time()
        
    # If answer is submitted, show results but don't prevent continued operation
    if st.session_state.answer_submitted:
        # Answer submitted, but user can continue viewing question and results
        pass
    
    # Display map
    if current_case.get('map_image_path'):
        # Modify map path handling
        map_path = current_case['map_image_path']
        if map_path.startswith('./'):
            # Path relative to project root, path now includes data directory
            map_path = os.path.join(
                os.getcwd(),
                map_path.replace('./', '')
            )
        
        if os.path.exists(map_path):
            st.markdown('<h4>🗺️ Scene Map</h4>', unsafe_allow_html=True)
            try:
                map_image = Image.open(map_path)
                # Create map container, limit maximum size
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        # Limit map size
                        st.image(map_image, use_container_width=True)
            except Exception as e:
                st.error(f"Unable to load map image: {str(e)}")
        else:
            st.warning(f"Map file does not exist: {map_path}")
    
    # Display camera images
    camera_images = current_case.get('camera_images', [])
    if camera_images:
        st.markdown('<h4>📹 Camera Images</h4>', unsafe_allow_html=True)
        
        # Display images for each camera
        for i, camera in enumerate(camera_images):
            camera_id = camera.get('camera_id', f'Camera_{i}')
            
            # For CausalReordering task, do not display time range
            if task_type == "CausalReordering":
                expander_title = f"📹 Camera {camera_id}"
            else:
                # Convert time format
            start_time_str = seconds_to_time_format(camera['start_timestamp'])
            end_time_str = seconds_to_time_format(camera['end_timestamp'])
                expander_title = f"📹 Camera {camera_id} (Time: {start_time_str} - {end_time_str})"
            
            with st.expander(expander_title):
                # Display video path information
                video_path = camera.get('video_path', '')
                
                # Handle relative paths, convert to absolute paths
                if video_path.startswith('./'):
                    # Path relative to project root, path now includes data directory
                    video_path = os.path.join(
                        os.getcwd(),
                        video_path.replace('./', '')
                    )
                
                st.write(f"**Video Path:** {video_path}")
                
                # Check if video file exists
                if os.path.exists(video_path):
                    st.success("✅ Video file exists")
                    
                    # Extract frames from video
                    frames = st.session_state.video_processor.extract_frames(
                        video_path,
                        camera['frame_ids'],
                        camera['bboxes']
                    )
                    
                    if frames:
                        # Display 3 evenly selected frames
                        cols = st.columns(3)
                        for j, frame in enumerate(frames):
                            with cols[j]:
                                st.image(frame, caption=f"Frame {camera['frame_ids'][j]}", use_container_width=True)
                    else:
                        st.warning(f"Unable to extract frames from video")
                        
                        # Try to get video information
                        video_info = st.session_state.video_processor.get_video_info(video_path)
                        if video_info:
                            st.write("**Video Information:**")
                            st.write(f"- Total Frames: {video_info['frame_count']}")
                            st.write(f"- Frame Rate: {video_info['fps']:.2f}")
                            st.write(f"- Resolution: {video_info['width']}x{video_info['height']}")
                            st.write(f"- Duration: {video_info['duration']:.2f} seconds")
                        
                        # Display requested frame IDs
                        st.write(f"**Requested Frame IDs:** {camera['frame_ids']}")
                        
                else:
                    st.error(f"❌ Video file does not exist: {video_path}")
    
    # Display question
    st.markdown('<h4>❓ Question</h4>', unsafe_allow_html=True)
    question = current_case.get('question', '')
    st.markdown(f'<div class="question-container">{question}</div>', unsafe_allow_html=True)
    
    # Display different answer interfaces based on task type
    display_question_interface(current_case, task_type)
    
    # Submit and navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Previous question button
        total_cases = len(st.session_state.data_loader.data.get('cases', []))
        if st.session_state.current_case_index > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_case_index -= 1
                st.session_state.user_answers = {}
                st.session_state.question_started = False
                st.session_state.answer_submitted = False
                st.session_state.start_time = None
                st.rerun()
        else:
            st.button("⬅️ Previous", disabled=True, use_container_width=True)
    
    with col2:
        if st.button("✅ Submit Answer", type="primary", use_container_width=True):
            submit_answer(current_case)
    
    with col3:
        # Next question button
            if st.session_state.current_case_index < total_cases - 1:
            if st.button("➡️ Next", use_container_width=True):
                st.session_state.current_case_index += 1
                st.session_state.user_answers = {}
                st.session_state.question_started = False
                st.session_state.answer_submitted = False
                st.session_state.start_time = None
                st.rerun()
            else:
            st.button("➡️ Next", disabled=True, use_container_width=True)
    
    # Display answer time
    if st.session_state.start_time:
        elapsed_time = time.time() - st.session_state.start_time
        st.info(f"⏱️ Answer Time: {elapsed_time:.1f} seconds")

def display_question_interface(case, task_type):
    """Display different answer interfaces based on task type"""
    
    # Display different interfaces based on task type
    if task_type in ["NextSpotForecasting", "MultiTrajectoryForecasting"]:
        # Choice + time range fill-in task
        display_option_and_time_fields(case)
    elif task_type == "TrajectoryForecasting":
        # Trajectory forecasting task (only trajectory forecasting fill-in)
        display_trajectory_forecasting_fields(case)
    else:
        # Pure multiple choice task
        display_option_only_fields(case)

def display_option_only_fields(case):
    """Display pure multiple choice interface"""
    choices = case.get('choices', [])
    if choices:
        st.markdown('<h4>🔘 Options</h4>', unsafe_allow_html=True)
        
        # Single choice
        selected_option = st.radio(
            "Choose the correct answer:",
            choices,
            index=st.session_state.user_answers.get('option_index', 0)
        )
        st.session_state.user_answers['option_index'] = choices.index(selected_option) if selected_option in choices else 0
        st.session_state.user_answers['options'] = [selected_option]

def display_option_and_time_fields(case):
    """Display option + time range fill-in interface"""
    choices = case.get('choices', [])
    if choices:
        st.markdown('<h4>🔘 Options</h4>', unsafe_allow_html=True)
        
        # Single choice
        selected_option = st.radio(
            "Choose the correct answer:",
            choices,
            index=st.session_state.user_answers.get('option_index', 0)
        )
        st.session_state.user_answers['option_index'] = choices.index(selected_option) if selected_option in choices else 0
        st.session_state.user_answers['options'] = [selected_option]
    
    # Display time range fill-in
    display_time_range_fields(case)

def display_time_range_fields(case):
    """Display time range fill-in questions"""
    st.markdown('<h4>⏰ Time Range Fill-in</h4>', unsafe_allow_html=True)
    
    # Check if there is time information
    time_fields = []
    
    # Check correct_time_str field
    if 'correct_time_str' in case and case['correct_time_str']:
        for i, time_str in enumerate(case['correct_time_str']):
            if '-' in time_str:
                start_time, end_time = time_str.split('-')
                time_fields.append((f'time_range_{i}_start', f'Time Range {i+1} Start Time', start_time))
                time_fields.append((f'time_range_{i}_end', f'Time Range {i+1} End Time', end_time))
            else:
                time_fields.append((f'time_range_{i}', f'Time Range {i+1}', time_str))
    
    # Check start_point and end_point fields
    if 'start_point' in case and case['start_point'].get('time'):
        time_fields.append(('start_time', 'Start Time', case['start_point']['time']))
    if 'end_point' in case and case['end_point'].get('time'):
        time_fields.append(('end_time', 'End Time', case['end_point']['time']))
    
    if time_fields:
        time_answers = {}
        
        for field_id, field_name, gt_time in time_fields:
            time_input = st.text_input(
                f"{field_name} (Format: HH:MM:SS.mmm)",
                value=st.session_state.user_answers.get(field_id, ''),
                help=f"Correct answer format: {gt_time}"
            )
            # Auto-correct time format (change colon to dot)
            if time_input and time_input.count(':') > 2:
                # If there are more than 2 colons, change the last colon to a dot
                parts = time_input.split(':')
                if len(parts) > 3:
                    time_input = ':'.join(parts[:-1]) + '.' + parts[-1]
            time_answers[field_id] = time_input
        
        st.session_state.user_answers.update(time_answers)
    else:
        st.info("This question has no time range fill-in requirements")

def display_trajectory_forecasting_fields(case):
    """Display trajectory forecasting fill-in questions"""
    st.markdown('<h4>🎯 Trajectory Forecasting</h4>', unsafe_allow_html=True)
    
    # Get options and correct answers
    choices = case.get('choices', [])
    correct_cam_names = case.get('correct_cam_name', [])
    correct_time_strs = case.get('correct_time_str', [])
    
    # First segment prediction
    st.markdown("**First Segment Prediction:**")
    
    # First camera selection
    if choices:
        first_camera_option = st.radio(
            "First Camera:",
            choices,
            index=st.session_state.user_answers.get('first_camera_index', 0),
            key="first_camera_radio"
        )
        first_camera_index = choices.index(first_camera_option) if first_camera_option in choices else 0
        first_camera = first_camera_option
    else:
        first_camera = st.text_input(
            "First Camera ID:",
            value=st.session_state.user_answers.get('first_camera', ''),
            help=f"Correct answer: {correct_cam_names[0] if len(correct_cam_names) > 0 else 'Unknown'}"
        )
        first_camera_index = 0
    
    # First time range
    if len(correct_time_strs) > 0:
        first_time_range = correct_time_strs[0]
        if '-' in first_time_range:
            first_start, first_end = first_time_range.split('-')
        else:
            first_start = first_end = first_time_range
    else:
        first_start = first_end = ""
    
    first_start_time = st.text_input(
        "First Segment Start Time (Format: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('first_start_time', ''),
        help=f"Correct answer: {first_start}"
    )
    # Auto-correct time format (change colon to dot)
    if first_start_time and first_start_time.count(':') > 2:
        # If there are more than 2 colons, change the last colon to a dot
        parts = first_start_time.split(':')
        if len(parts) > 3:
            first_start_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    first_end_time = st.text_input(
        "First Segment End Time (Format: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('first_end_time', ''),
        help=f"Correct answer: {first_end}"
    )
    # Auto-correct time format (change colon to dot)
    if first_end_time and first_end_time.count(':') > 2:
        # If there are more than 2 colons, change the last colon to a dot
        parts = first_end_time.split(':')
        if len(parts) > 3:
            first_end_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    # Second segment prediction
    st.markdown("**Second Segment Prediction:**")
    
    # Second camera selection
    if choices:
        second_camera_option = st.radio(
            "Second Camera:",
            choices,
            index=st.session_state.user_answers.get('second_camera_index', 0),
            key="second_camera_radio"
        )
        second_camera_index = choices.index(second_camera_option) if second_camera_option in choices else 0
        second_camera = second_camera_option
    else:
        second_camera = st.text_input(
            "Second Camera ID:",
            value=st.session_state.user_answers.get('second_camera', ''),
            help=f"Correct answer: {correct_cam_names[1] if len(correct_cam_names) > 1 else 'Unknown'}"
        )
        second_camera_index = 0
    
    # Second time range
    if len(correct_time_strs) > 1:
        second_time_range = correct_time_strs[1]
        if '-' in second_time_range:
            second_start, second_end = second_time_range.split('-')
        else:
            second_start = second_end = second_time_range
    else:
        second_start = second_end = ""
    
    second_start_time = st.text_input(
        "Second Segment Start Time (Format: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('second_start_time', ''),
        help=f"Correct answer: {second_start}"
    )
    # Auto-correct time format (change colon to dot)
    if second_start_time and second_start_time.count(':') > 2:
        # If there are more than 2 colons, change the last colon to a dot
        parts = second_start_time.split(':')
        if len(parts) > 3:
            second_start_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    second_end_time = st.text_input(
        "Second Segment End Time (Format: HH:MM:SS.mmm):",
        value=st.session_state.user_answers.get('second_end_time', ''),
        help=f"Correct answer: {second_end}"
    )
    # Auto-correct time format (change colon to dot)
    if second_end_time and second_end_time.count(':') > 2:
        # If there are more than 2 colons, change the last colon to a dot
        parts = second_end_time.split(':')
        if len(parts) > 3:
            second_end_time = ':'.join(parts[:-1]) + '.' + parts[-1]
    
    # Save answers
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
    """Submit answer and calculate score"""
    end_time = time.time()
    elapsed_time = end_time - st.session_state.start_time
    
    # Calculate score
    score_result = st.session_state.scoring_system.calculate_score_new(
        current_case,
        st.session_state.user_answers,
        elapsed_time
    )
    
    # Save results
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
    
    # Display results
    show_result(result, current_case)
    
    # Set answer submitted state
    st.session_state.answer_submitted = True

def show_result(result, current_case):
    """Display answer results"""
    st.markdown('<h3 class="sub-header">📊 Answer Results</h3>', unsafe_allow_html=True)
    
    if result['accuracy_score'] > 0:
        st.markdown('<div class="result-correct">✅ Correct Answer!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-incorrect">❌ Incorrect Answer</div>', unsafe_allow_html=True)
    
    # Display detailed information
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Score", f"{result['score']:.2f}")
        st.metric("Accuracy Score", f"{result['accuracy_score']:.2f}")
        st.metric("Time Score", f"{result['time_score']:.2f}")
    
    with col2:
        st.metric("Answer Time", f"{result['elapsed_time']:.1f} seconds")
        st.metric("Question Type", result['task_type'])
        st.metric("Question ID", result['case_id'])
    
    # Display correct answers
    st.markdown('<h4>📋 Correct Answers</h4>', unsafe_allow_html=True)
    
    # Directly display correct_cam_name and correct_time_str fields
    correct_cam_names = current_case.get('correct_cam_name', [])
    correct_time_strs = current_case.get('correct_time_str', [])
    
    if correct_cam_names:
        st.info(f"**correct_cam_name:** {correct_cam_names}")
    
    if correct_time_strs:
        st.info(f"**correct_time_str:** {correct_time_strs}")
    
    # If these fields don't exist, display ground_truth
    if not correct_cam_names and not correct_time_strs:
        ground_truth = current_case.get('ground_truth', '')
        st.info(f"**ground_truth:** {ground_truth}")
    
    # Display user answers
    st.markdown('<h4>👤 Your Answers</h4>', unsafe_allow_html=True)
    user_answers = result['user_answers']
    
    if 'options' in user_answers:
        st.write(f"**Option Answers:** {', '.join(user_answers['options'])}")
    
    time_answers = {k: v for k, v in user_answers.items() if k.endswith('_time')}
    if time_answers:
        st.write("**Time Answers:**")
        for field, answer in time_answers.items():
            st.write(f"- {field}: {answer}")
    
    # Display trajectory forecasting answers
    trajectory_fields = ['first_camera', 'first_start_time', 'first_end_time', 
                        'second_camera', 'second_start_time', 'second_end_time']
    trajectory_answers = {k: v for k, v in user_answers.items() if k in trajectory_fields}
    if trajectory_answers:
        st.write("**Trajectory Forecasting Answers:**")
        
        # First segment
        first_camera = trajectory_answers.get('first_camera', '')
        first_start = trajectory_answers.get('first_start_time', '')
        first_end = trajectory_answers.get('first_end_time', '')
        if first_camera:
            st.write(f"📹 **First Camera ID:** {first_camera}")
            if first_start and first_end:
                st.write(f"⏰ **First Time Range:** {first_start} - {first_end}")
            elif first_start:
                st.write(f"⏰ **First Time:** {first_start}")
        
        # Second segment
        second_camera = trajectory_answers.get('second_camera', '')
        second_start = trajectory_answers.get('second_start_time', '')
        second_end = trajectory_answers.get('second_end_time', '')
        if second_camera:
            st.write(f"📹 **Second Camera ID:** {second_camera}")
            if second_start and second_end:
                st.write(f"⏰ **Second Time Range:** {second_start} - {second_end}")
            elif second_start:
                st.write(f"⏰ **Second Time:** {second_start}")

def show_results_summary():
    """Display answer results summary"""
    if not st.session_state.results:
        st.warning("No answer records yet")
        return
    
    st.markdown('<h3 class="sub-header">📈 Answer Results Summary</h3>', unsafe_allow_html=True)
    
    # Create results DataFrame
    df = pd.DataFrame(st.session_state.results)
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Questions", len(df))
    
    with col2:
        correct_count = len(df[df['accuracy_score'] > 0])
        st.metric("Correct Questions", correct_count)
    
    with col3:
        accuracy = correct_count / len(df) * 100 if len(df) > 0 else 0
        st.metric("Accuracy Rate", f"{accuracy:.1f}%")
    
    with col4:
        avg_score = df['score'].mean() if len(df) > 0 else 0
        st.metric("Average Score", f"{avg_score:.2f}")
    
    # Display detailed results table
    st.markdown('<h4>📋 Detailed Results</h4>', unsafe_allow_html=True)
    
    # Simplify display columns
    display_df = df[['case_id', 'task_type', 'score', 'accuracy_score', 'time_score', 'elapsed_time']].copy()
    display_df['elapsed_time'] = display_df['elapsed_time'].round(1)
    display_df['score'] = display_df['score'].round(2)
    display_df['accuracy_score'] = display_df['accuracy_score'].round(2)
    display_df['time_score'] = display_df['time_score'].round(2)
    
    st.dataframe(display_df, use_container_width=True)
    
    # Export results
    if st.button("📥 Export Results"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name=f"answer_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


def display_results_visualization():
    """Display results visualization interface"""
    st.markdown('<h2 class="sub-header">📊 Evaluation Results Visualization</h2>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'results_data' not in st.session_state:
        st.session_state.results_data = {}
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = None
    if 'selected_scene' not in st.session_state:
        st.session_state.selected_scene = None
    if 'selected_task' not in st.session_state:
        st.session_state.selected_task = None
    
    # Result file selection
    st.markdown('<h3>📁 Select Result File</h3>', unsafe_allow_html=True)
    
    # Find result files
    result_files = []
    eval_dir = "./eval/results"
    if os.path.exists(eval_dir):
        for file in os.listdir(eval_dir):
            if file.endswith('.json') and not file.startswith('prompt_'):
                result_files.append(file)
    
    if not result_files:
        st.warning("No evaluation result files found, please run evaluation script first")
        if st.button("🔙 Return to Main Interface"):
            st.session_state.show_results = False
            st.rerun()
        return
    
    # Result file selection
    selected_file = st.selectbox("Select Evaluation Result File", result_files, index=0)
    
    if selected_file != st.session_state.get('selected_file'):
        st.session_state.selected_file = selected_file
        st.session_state.results_data = {}
        st.rerun()
    
    # Load selected result file
    if st.session_state.selected_file and st.session_state.selected_file not in st.session_state.results_data:
        file_path = os.path.join(eval_dir, st.session_state.selected_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            st.session_state.results_data[st.session_state.selected_file] = data
            st.success(f"✅ Successfully loaded evaluation result file: {st.session_state.selected_file}")
        except Exception as e:
            st.error(f"❌ Failed to load result file: {str(e)}")
            return
    
    # Display results statistics
    if st.session_state.selected_file in st.session_state.results_data:
        results = st.session_state.results_data[st.session_state.selected_file]
        # Extract model name from filename for display
        model_name = st.session_state.selected_file.split('_')[0] + '_' + st.session_state.selected_file.split('_')[1] if '_' in st.session_state.selected_file else st.session_state.selected_file.split('_')[0]
        display_results_statistics(results, model_name)
        
        # Scene and task type filtering
        st.markdown('<h3>🔍 Result Filtering</h3>', unsafe_allow_html=True)
        
        # Get all scenes and task types
        scenes = list(set([r.get('scene', 'unknown') for r in results]))
        task_types = list(set([r.get('task_id', 'unknown') for r in results]))  # Use task_id field
        
        col1, col2 = st.columns(2)
        with col1:
            selected_scene = st.selectbox("Select Scene", ["All"] + scenes, index=0)
        with col2:
            selected_task = st.selectbox("Select Task Type", ["All"] + task_types, index=0)
        
        # Filter results
        filtered_results = results
        if selected_scene != "All":
            filtered_results = [r for r in filtered_results if r.get('scene') == selected_scene]
        if selected_task != "All":
            filtered_results = [r for r in filtered_results if r.get('task_id') == selected_task]  # Use task_id field
        
        # Display detailed results
        if filtered_results:
            display_detailed_results(filtered_results, selected_scene, selected_task)
        else:
            st.info("No results matching the criteria")
    
    # Return button
    if st.button("🔙 Return to Main Interface"):
        st.session_state.show_results = False
        st.rerun()

def display_results_statistics(results, model_name):
    """Display results statistics"""
    st.markdown('<h3>📈 Overall Statistics</h3>', unsafe_allow_html=True)
    
    total_cases = len(results)
    correct_cases = sum(1 for r in results if r.get('metrics', {}).get('MCQacc', 0) > 0)
    avg_score = sum(r.get('metrics', {}).get('score', 0) for r in results) / total_cases if total_cases > 0 else 0
    avg_mcq = sum(r.get('metrics', {}).get('MCQacc', 0) for r in results) / total_cases if total_cases > 0 else 0
    avg_time_iou = sum(r.get('metrics', {}).get('TimeIoU', 0) for r in results) / total_cases if total_cases > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Model", model_name)
    with col2:
        st.metric("Total Questions", total_cases)
    with col3:
        st.metric("Correct Questions", correct_cases)
    with col4:
        st.metric("Average Score", f"{avg_score:.3f}")
    with col5:
        st.metric("Average MCQ", f"{avg_mcq:.3f}")
    
    # Statistics by scene
    st.markdown('<h4>📊 Statistics by Scene</h4>', unsafe_allow_html=True)
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
            'Scene': scene,
            'Questions': stats['total'],
            'Correct': stats['correct'],
            'Accuracy': f"{stats['correct']/stats['total']*100:.1f}%" if stats['total'] > 0 else "0%",
            'Avg Score': f"{sum(stats['scores'])/len(stats['scores']):.3f}" if stats['scores'] else "0.000",
            'Avg MCQ': f"{sum(stats['mcqs'])/len(stats['mcqs']):.3f}" if stats['mcqs'] else "0.000"
        }
        for scene, stats in scene_stats.items()
    ])
    
    st.dataframe(scene_df, use_container_width=True)
    
    # Statistics by task type
    st.markdown('<h4>📊 Statistics by Task Type</h4>', unsafe_allow_html=True)
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
            'Task Type': task,
            'Questions': stats['total'],
            'Correct': stats['correct'],
            'Accuracy': f"{stats['correct']/stats['total']*100:.1f}%" if stats['total'] > 0 else "0%",
            'Avg Score': f"{sum(stats['scores'])/len(stats['scores']):.3f}" if stats['scores'] else "0.000",
            'Avg MCQ': f"{sum(stats['mcqs'])/len(stats['mcqs']):.3f}" if stats['mcqs'] else "0.000"
        }
        for task, stats in task_stats.items()
    ])
    
    st.dataframe(task_df, use_container_width=True)

def display_detailed_results(results, scene_filter, task_filter):
    """Display detailed results"""
    st.markdown('<h3>📋 Detailed Results</h3>', unsafe_allow_html=True)
    
    # Create results table
    display_data = []
    for result in results:
        # Get ground_truth
        ground_truth = result.get('response', {}).get('ground_truth', {})
        if isinstance(ground_truth, dict):
            ground_truth_str = str(ground_truth)
        else:
            ground_truth_str = str(ground_truth)
        
        display_data.append({
            'Case ID': result.get('case_id', ''),
            'Scene': result.get('scene', ''),
            'Task Type': result.get('task_id', ''),  # Use task_id field
            'Score': f"{result.get('metrics', {}).get('score', 0):.3f}",
            'MCQ': f"{result.get('metrics', {}).get('MCQacc', 0):.3f}",
            'TimeIoU': f"{result.get('metrics', {}).get('TimeIoU', 0):.3f}",
            'Model Answer': result.get('response', {}).get('model_answer', '')[:100] + '...' if len(result.get('response', {}).get('model_answer', '')) > 100 else result.get('response', {}).get('model_answer', ''),
            'Extracted Answer': str(result.get('response', {}).get('answer', [])),
            'Time Range': str(result.get('response', {}).get('time_duration', [])),
            'Ground Truth': ground_truth_str[:100] + '...' if len(ground_truth_str) > 100 else ground_truth_str
        })
    
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True)
    
    # Add question detail viewing functionality
    st.markdown('<h4>🔍 View Question Details</h4>', unsafe_allow_html=True)
    
    # Select case to view
    case_ids = [result.get('case_id', '') for result in results]
    selected_case_id = st.selectbox("Select Case ID to view details", case_ids, index=0)
    
    if selected_case_id:
        # Find selected case from results
        selected_result = next((r for r in results if r.get('case_id') == selected_case_id), None)
        if selected_result:
            display_case_details(selected_result)
    
    # Export functionality
    if st.button("📥 Export Results"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name=f"evaluation_results_{scene_filter}_{task_filter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def display_case_details(result):
    """Display detailed information for a single case"""
    case_id = result.get('case_id', '')
    scene = result.get('scene', '')
    task_type = result.get('task_id', '')  # Use task_id field
    
    st.markdown(f'<h5>📝 Case Details: {case_id}</h5>', unsafe_allow_html=True)
    
    # Try to load question details from original data
    try:
        # Build data file path
        data_file = f"data/{scene}/{scene}_{task_type}_30.json"
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Find corresponding case
            case_data = None
            for case in data.get('cases', []):
                if case.get('case_id') == case_id:
                    case_data = case
                    break
            
            if case_data:
                # Display question content
                st.markdown('<h6>📋 Question Content</h6>', unsafe_allow_html=True)
                st.write(case_data.get('question', ''))
                
                # Display options
                choices = case_data.get('choices', [])
                if choices:
                    st.markdown('<h6>🔘 Options</h6>', unsafe_allow_html=True)
                    for i, choice in enumerate(choices):
                        st.write(f"{chr(65+i)}. {choice}")
                
                # Display map image
                if case_data.get('map_image_path'):
                    st.markdown('<h6>🗺️ Scene Map</h6>', unsafe_allow_html=True)
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
                            st.error(f"Unable to load map image: {str(e)}")
                    else:
                        st.warning(f"Map file does not exist: {map_path}")
                
                # Display camera images
                camera_images = case_data.get('camera_images', [])
                if camera_images:
                    st.markdown('<h6>📹 Camera Images</h6>', unsafe_allow_html=True)
                    
                    for i, camera in enumerate(camera_images):
                        camera_id = camera.get('camera_id', f'Camera_{i}')
                        
                        # For CausalReordering task, do not display time range
                        if task_type == "CausalReordering":
                            expander_title = f"📹 Camera {camera_id}"
                        else:
                            # Convert time format
                            start_time_str = seconds_to_time_format(camera['start_timestamp'])
                            end_time_str = seconds_to_time_format(camera['end_timestamp'])
                            expander_title = f"📹 Camera {camera_id} (Time: {start_time_str} - {end_time_str})"
                        
                        with st.expander(expander_title):
                            # Display video path information
                            video_path = camera.get('video_path', '')
                            
                            # Handle relative paths, convert to absolute paths
                            if video_path.startswith('./'):
                                video_path = os.path.join(
                                    os.getcwd(),
                                    video_path.replace('./', '')
                                )
                            
                            st.write(f"**Video Path:** {video_path}")
                            
                            # Check if video file exists
                            if os.path.exists(video_path):
                                st.success("✅ Video file exists")
                                
                                # Extract frames from video
                                frames = st.session_state.video_processor.extract_frames(
                                    video_path,
                                    camera['frame_ids'],
                                    camera['bboxes']
                                )
                                
                                if frames:
                                    # Display 3 evenly selected frames
                                    cols = st.columns(3)
                                    for j, frame in enumerate(frames):
                                        with cols[j]:
                                            st.image(frame, caption=f"Frame {camera['frame_ids'][j]}", use_container_width=True)
                                else:
                                    st.warning(f"Unable to extract frames from video")
                            else:
                                st.error(f"❌ Video file does not exist: {video_path}")
            else:
                st.warning(f"Original data for case {case_id} not found")
        else:
            st.warning(f"Data file does not exist: {data_file}")
    except Exception as e:
        st.error(f"Error loading question details: {str(e)}")
    
    # Display evaluation results
    st.markdown('<h6>📊 Evaluation Results</h6>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{result.get('metrics', {}).get('score', 0):.3f}")
    with col2:
        st.metric("MCQ", f"{result.get('metrics', {}).get('MCQacc', 0):.3f}")
    with col3:
        st.metric("TimeIoU", f"{result.get('metrics', {}).get('TimeIoU', 0):.3f}")
    
    # Display model answer
    st.markdown('<h6>🤖 Model Answer</h6>', unsafe_allow_html=True)
    model_answer = result.get('response', {}).get('model_answer', '')
    st.text_area("Model Raw Response", model_answer, height=200, disabled=True)
    
    # Display extracted answers
    st.markdown('<h6>📝 Extracted Answers</h6>', unsafe_allow_html=True)
    extracted_answer = result.get('response', {}).get('answer', [])
    time_duration = result.get('response', {}).get('time_duration', [])
    
    st.write(f"**Multiple Choice Answers**: {extracted_answer}")
    st.write(f"**Time Range**: {time_duration}")
    
    # Display correct answers
    st.markdown('<h6>✅ Correct Answers</h6>', unsafe_allow_html=True)
    ground_truth = result.get('response', {}).get('ground_truth', {})
    st.write(f"**Ground Truth**: {ground_truth}")

def display_eval_interface():
    """Display model evaluation interface"""
    st.markdown('<h2 class="sub-header">🤖 Model Evaluation System</h2>', unsafe_allow_html=True)
    
    # Return button
    if st.button("🔙 Return to Main Interface"):
        st.session_state.show_eval = False
        st.rerun()
    
    # Evaluation configuration
    st.markdown('<h3>⚙️ Evaluation Configuration</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model configuration
        st.markdown('<h4>🔧 Model Configuration</h4>', unsafe_allow_html=True)
        model_name = st.text_input("Model Name", help="e.g.: claude-sonnet-4-20250514-thinking, gpt-4o")
        api_key = st.text_input("API Key", type="password", help="OpenAI API key")
        base_url = st.text_input("Base URL", help="API base URL")
        
        # Model parameters
        st.markdown('<h4>🎛️ Model Parameters</h4>', unsafe_allow_html=True)
        max_tokens = st.number_input("Max Tokens", min_value=1, max_value=32768, value=16384)
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.1, step=0.1)
    
    with col2:
        # Test configuration
        st.markdown('<h4>📋 Test Configuration</h4>', unsafe_allow_html=True)
        
        # Test scope selection
        test_scope = st.radio(
            "Test Scope",
            ["Specific Scene-Task", "All Scenes-Tasks"],
            help="Choose specific scene-task or all scene-tasks"
        )
        
        if test_scope == "Specific Scene-Task":
            # Specific scene-task selection
            scene = st.selectbox("Scene", ["indoor", "outdoor"])
            task_type = st.selectbox(
                "Task Type",
                ["MotionState", "GeoLocation", "ArrivalTimeInterval", "CausalReordering", 
                 "TrajectoryForecasting", "NextSpotForecasting", "MultiTargetTrajectoryForecasting"]
            )
            max_cases = st.number_input("Test Cases", min_value=1, max_value=30, value=5)
            
            # Calculate total cases
            total_cases = max_cases
            
        else:
            # All scenes-tasks
            max_cases_per_scene = st.number_input("Test Cases per Scene", min_value=1, max_value=30, value=5)
            
            # Calculate total cases (2 scenes × 7 task types × cases per scene)
            total_cases = 2 * 7 * max_cases_per_scene
    
    # Display estimated information
    st.info(f"📊 Estimated Total Test Cases: {total_cases}")
    
    # Start evaluation and stop evaluation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Start Evaluation", type="primary", use_container_width=True):
            if not model_name or not api_key or not base_url:
                st.error("❌ Please fill in complete model configuration information")
            else:
                start_evaluation(model_name, api_key, base_url, max_tokens, temperature, 
                               test_scope, scene if test_scope == "Specific Scene-Task" else None,
                               task_type if test_scope == "Specific Scene-Task" else None,
                               max_cases if test_scope == "Specific Scene-Task" else max_cases_per_scene)
    
    with col2:
        if st.button("⏹️ Stop Evaluation", use_container_width=True):
            stop_evaluation()
    
    # Display evaluation progress
    if st.session_state.eval_status == "running":
        display_eval_progress()
    elif st.session_state.eval_status == "completed":
        display_eval_completion()
    elif st.session_state.eval_status == "error":
        display_eval_error()

def start_evaluation(model_name, api_key, base_url, max_tokens, temperature, test_scope, scene, task_type, max_cases):
    """Start evaluation"""
    st.session_state.eval_status = "running"
    st.session_state.eval_progress = 0
    st.session_state.eval_total = 0
    st.session_state.eval_output = []
    
    # Build eval.py command
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
    
    if test_scope == "Specific Scene-Task":
        cmd.extend(["--scene", scene, "--task-type", task_type])
    
    # Use queues to pass data between threads
    output_queue = queue.Queue()
    status_queue = queue.Queue()
    
    # Run evaluation in background thread
    def run_eval():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output
            for line in iter(process.stdout.readline, ''):
                if line:
                    output_queue.put(line.strip())
                    
                    # Parse progress information
                    if "Processing case" in line:
                        # Extract current progress
                        try:
                            parts = line.split("Processing case ")[1].split("/")
                            current = int(parts[0])
                            total = int(parts[1].split(":")[0])
                            status_queue.put(("progress", current, total))
                        except:
                            pass
            
            # Wait for process to complete
            return_code = process.wait()
            
            if return_code == 0:
                status_queue.put(("status", "completed"))
            else:
                status_queue.put(("status", "error"))
                
        except Exception as e:
            output_queue.put(f"Error: {str(e)}")
            status_queue.put(("status", "error"))
    
    # Start background thread
    thread = threading.Thread(target=run_eval)
    thread.daemon = True
    thread.start()
    
    # Store queues in session_state
    st.session_state.eval_output_queue = output_queue
    st.session_state.eval_status_queue = status_queue
    
    st.success("✅ Evaluation started, please check progress information below")

def stop_evaluation():
    """Stop evaluation"""
    if 'eval_process' in st.session_state and st.session_state.eval_process:
        try:
            st.session_state.eval_process.terminate()
            st.session_state.eval_status = "stopped"
            st.success("⏹️ Evaluation stopped")
        except Exception as e:
            st.error(f"Error stopping evaluation: {str(e)}")
    else:
        st.warning("No running evaluation process")

def display_eval_progress():
    """Display evaluation progress"""
    st.markdown('<h3>📊 Evaluation Progress</h3>', unsafe_allow_html=True)
    
    # Process data from queue
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
    
    # Progress bar
    if st.session_state.eval_total > 0:
        progress = st.session_state.eval_progress / st.session_state.eval_total
        st.progress(progress)
        st.write(f"Progress: {st.session_state.eval_progress}/{st.session_state.eval_total} ({progress*100:.1f}%)")
    else:
        st.progress(0)
        st.write("Initializing...")
    
    # Display prompt file paths
    st.markdown('<h4>📁 Prompt File Paths</h4>', unsafe_allow_html=True)
    
    # Extract prompt file paths from output
    prompt_files = []
    if st.session_state.eval_output:
        for line in st.session_state.eval_output:
            if "完整对话记录已导出到:" in line:
                file_path = line.split("完整对话记录已导出到: ")[1]
                prompt_files.append(file_path)
    
    if prompt_files:
        # Display latest prompt file paths
        recent_files = prompt_files[-5:]  # Show latest 5 files
        for file_path in recent_files:
            st.text(f"📄 {file_path}")
    else:
        st.info("No prompt files generated yet")
    
    # Auto refresh
    time.sleep(1)
    st.rerun()

def display_eval_completion():
    """Display evaluation completion"""
    st.markdown('<h3>✅ Evaluation Completed</h3>', unsafe_allow_html=True)
    
    # Display final output
    st.markdown('<h4>📝 Final Output</h4>', unsafe_allow_html=True)
    
    if st.session_state.eval_output:
        # Display all output
        for line in st.session_state.eval_output:
            if "Error" in line or "Failed" in line:
                st.error(line)
            elif "Completed" in line or "Success" in line:
                st.success(line)
            elif "Processing case" in line:
                st.info(line)
            else:
                st.text(line)
    
    # Reset status button
    if st.button("🔄 Restart Evaluation"):
        st.session_state.eval_status = "idle"
        st.session_state.eval_output = []
        st.session_state.eval_progress = 0
        st.session_state.eval_total = 0
        # Clear queues
        if 'eval_output_queue' in st.session_state:
            del st.session_state.eval_output_queue
        if 'eval_status_queue' in st.session_state:
            del st.session_state.eval_status_queue
        st.rerun()
    
    # View results button
    if st.button("📈 View Evaluation Results"):
        st.session_state.show_eval = False
        st.session_state.show_results = True
        st.rerun()

def display_eval_error():
    """Display evaluation error"""
    st.markdown('<h3>❌ Evaluation Error</h3>', unsafe_allow_html=True)
    
    # Display error output
    st.markdown('<h4>📝 Error Information</h4>', unsafe_allow_html=True)
    
    if st.session_state.eval_output:
        for line in st.session_state.eval_output:
            st.error(line)
    
    # Reset status button
    if st.button("🔄 Restart Evaluation"):
        st.session_state.eval_status = "idle"
        st.session_state.eval_output = []
        st.session_state.eval_progress = 0
        st.session_state.eval_total = 0
        # Clear queues
        if 'eval_output_queue' in st.session_state:
            del st.session_state.eval_output_queue
        if 'eval_status_queue' in st.session_state:
            del st.session_state.eval_status_queue
        st.rerun()

def display_ground_truth(case, task_type):
    """Display correct GT information based on task type"""
    
    # Process task type to ensure correct format
    if task_type == "Next Spot Forecasting":
        task_type = "NextSpotForecasting"
    elif task_type == "Trajectory Forecasting":
        task_type = "TrajectoryForecasting"
    elif task_type == "Multi Trajectory Forecasting" or task_type == "Multi-Target Trajectory Forecasting":
        task_type = "MultiTrajectoryForecasting"
    elif ' ' in task_type:
        task_type = task_type.split()[-1]
    
    # Pure multiple choice tasks: only display option answers
    if task_type in ["MotionState", "GeoLocation", "ArrivalTimeInterval", "CausalReordering"]:
        # Try to get from correct_cam_name, if not available then from ground_truth
        correct_cam_names = case.get('correct_cam_name', [])
        if correct_cam_names:
            st.info(f"**Correct Answer:** {correct_cam_names[0]}")
        else:
            ground_truth = case.get('ground_truth', '')
            st.info(f"**Correct Answer:** {ground_truth}")
    
    # Choice + fill-in tasks: display camera selection and time range
    elif task_type in ["NextSpotForecasting", "MultiTrajectoryForecasting"]:
        correct_cam_names = case.get('correct_cam_name', [])
        correct_time_strs = case.get('correct_time_str', [])
        
        if correct_cam_names:
            st.info(f"**Camera Answer:** {correct_cam_names[0]}")
        
        if correct_time_strs:
            for i, time_str in enumerate(correct_time_strs):
                if '-' in time_str:
                    start_time, end_time = time_str.split('-')
                    st.info(f"**Time Range {i+1}:** {start_time} - {end_time}")
                else:
                    st.info(f"**Time Point {i+1}:** {time_str}")
    
    # Trajectory forecasting task: display two cameras and two time ranges
    elif task_type == "TrajectoryForecasting":
        correct_cam_names = case.get('correct_cam_name', [])
        correct_time_strs = case.get('correct_time_str', [])
        
        if correct_cam_names and len(correct_cam_names) >= 2:
            st.info(f"**First Segment Camera:** {correct_cam_names[0]}")
            st.info(f"**Second Segment Camera:** {correct_cam_names[1]}")
        
        if correct_time_strs and len(correct_time_strs) >= 2:
            # First time
            first_time = correct_time_strs[0]
            if '-' in first_time:
                start_time, end_time = first_time.split('-')
                st.info(f"**First Time Range:** {start_time} - {end_time}")
            else:
                st.info(f"**First Time Point:** {first_time}")
            
            # Second time
            second_time = correct_time_strs[1]
            if '-' in second_time:
                start_time, end_time = second_time.split('-')
                st.info(f"**Second Time Range:** {start_time} - {end_time}")
            else:
                st.info(f"**Second Time Point:** {second_time}")
    
    else:
        # Default case
        ground_truth = case.get('ground_truth', '')
        st.info(f"**Correct Answer:** {ground_truth}")

if __name__ == "__main__":
    main()
