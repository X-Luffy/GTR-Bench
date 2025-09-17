import streamlit as st
from PIL import Image
import os
from typing import Dict, List

class QuestionDisplay:
    """题目显示组件类"""
    
    @staticmethod
    def display_map(case: Dict) -> None:
        """显示地图"""
        if case.get('map_image_path'):
            map_path = os.path.join(
                "/home/mnt/xieqinghongbing/data/question_generation/benchmark/selected",
                case['map_image_path'].replace('./', '')
            )
            if os.path.exists(map_path):
                st.markdown('<h4>🗺️ 场景地图</h4>', unsafe_allow_html=True)
                map_image = Image.open(map_path)
                st.image(map_image, use_column_width=True)
    
    @staticmethod
    def display_cameras(case: Dict, video_processor) -> None:
        """显示摄像头图像"""
        camera_images = case.get('camera_images', [])
        if camera_images:
            st.markdown('<h4>📹 摄像头图像</h4>', unsafe_allow_html=True)
            
            for i, camera in enumerate(camera_images):
                with st.expander(f"摄像头 {camera['camera_id']} (时间: {camera['start_timestamp']:.3f}s - {camera['end_timestamp']:.3f}s)"):
                    # 从视频中提取帧
                    frames = video_processor.extract_frames(
                        camera['crop_video_path'],
                        camera['frame_ids'],
                        camera['bboxes']
                    )
                    
                    if frames:
                        # 显示3张均匀选择的帧
                        cols = st.columns(3)
                        for j, frame in enumerate(frames):
                            with cols[j]:
                                st.image(frame, caption=f"帧 {camera['frame_ids'][j]}", use_column_width=True)
                    else:
                        st.warning(f"无法加载摄像头 {camera['camera_id']} 的视频帧")
    
    @staticmethod
    def display_question(case: Dict) -> None:
        """显示问题"""
        st.markdown('<h4>❓ 问题</h4>', unsafe_allow_html=True)
        question = case.get('question_cn', case.get('question', ''))
        st.markdown(f'<div class="question-container">{question}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_choices(case: Dict, user_answers: Dict) -> None:
        """显示选项"""
        choices = case.get('choices_cn', case.get('choices', []))
        if choices:
            st.markdown('<h4>🔘 选项</h4>', unsafe_allow_html=True)
            
            # 根据题目类型决定单选还是多选
            question_type = case.get('question_type', '')
            if 'timeline' in question_type.lower() or 'forecasting' in question_type.lower():
                # 多选
                selected_options = st.multiselect(
                    "选择正确答案（可多选）:",
                    choices,
                    default=user_answers.get('options', [])
                )
                user_answers['options'] = selected_options
            else:
                # 单选
                selected_option = st.radio(
                    "选择正确答案:",
                    choices,
                    index=user_answers.get('option_index', 0)
                )
                user_answers['option_index'] = choices.index(selected_option) if selected_option in choices else 0
                user_answers['options'] = [selected_option]
    
    @staticmethod
    def display_time_fields(case: Dict, user_answers: Dict) -> None:
        """显示时间填空题"""
        time_fields = []
        if 'start_point' in case and case['start_point'].get('time'):
            time_fields.append(('start_time', '开始时间', case['start_point']['time']))
        if 'end_point' in case and case['end_point'].get('time'):
            time_fields.append(('end_time', '结束时间', case['end_point']['time']))
        if 'middle_point' in case and case['middle_point'].get('time'):
            time_fields.append(('middle_time', '中间时间', case['middle_point']['time']))
        
        if time_fields:
            st.markdown('<h4>⏰ 时间填空</h4>', unsafe_allow_html=True)
            time_answers = {}
            
            for field_id, field_name, gt_time in time_fields:
                # 解析GT时间格式
                if '-' in gt_time:
                    start_time, end_time = gt_time.split('-')
                    time_input = st.text_input(
                        f"{field_name} (格式: HH:MM:SS.mmm)",
                        value=user_answers.get(field_id, ''),
                        help=f"正确答案格式: {gt_time}"
                    )
                    time_answers[field_id] = time_input
                else:
                    time_input = st.text_input(
                        f"{field_name} (格式: HH:MM:SS.mmm)",
                        value=user_answers.get(field_id, ''),
                        help=f"正确答案: {gt_time}"
                    )
                    time_answers[field_id] = time_input
            
            user_answers.update(time_answers)
    
    @staticmethod
    def display_submit_button() -> bool:
        """显示提交按钮"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            return st.button("✅ 提交答案", type="primary", use_container_width=True)
