import cv2
import numpy as np
from PIL import Image
import os
from typing import List, Optional, Tuple

class VideoProcessor:
    """视频处理器类，负责从视频中提取帧并绘制边界框"""
    
    def __init__(self):
        self.cache = {}  # 简单的内存缓存
    
    def extract_frames(self, video_path: str, frame_ids: List[int], bboxes: List[List[float]]) -> List[Image.Image]:
        """
        从视频或帧文件夹中提取指定帧并绘制边界框
        
        Args:
            video_path: Video file path或帧文件夹路径
            frame_ids: 帧ID列表
            bboxes: List of bounding boxes，格式为 [x, y, width, height]
            
        Returns:
            处理后的图像列表
        """
        if not os.path.exists(video_path):
            print(f"路径不存在: {video_path}")
            return []
        
        # 检查缓存
        cache_key = f"{video_path}_{hash(tuple(frame_ids))}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 判断是视频文件还是帧文件夹
        if os.path.isfile(video_path):
            # cityflow场景：从视频文件中提取帧
            return self._extract_frames_from_video(video_path, frame_ids, bboxes, cache_key)
        elif os.path.isdir(video_path):
            # mtmmc场景：从帧文件夹中读取帧图片
            return self._extract_frames_from_folder(video_path, frame_ids, bboxes, cache_key)
        else:
            print(f"路径既不是文件也不是文件夹: {video_path}")
            return []
    
    def _extract_frames_from_video(self, video_path: str, frame_ids: List[int], bboxes: List[List[float]], cache_key: str) -> List[Image.Image]:
        """
        从视频文件中提取帧（cityflow场景）
        """
        try:
            # 打开视频
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Cannot open video file: {video_path}")
                return []
            
            # 获取视频信息
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f"视频信息: 总帧数={total_frames}, 帧率={fps}")
            
            frames = []
            
            # 均匀选择3帧显示
            if len(frame_ids) > 3:
                step = len(frame_ids) // 3
                selected_indices = [0, step, len(frame_ids) - 1]
            else:
                selected_indices = list(range(len(frame_ids)))
            
            print(f"选择的帧索引: {selected_indices}")
            print(f"请求的帧ID: {frame_ids}")
            
            for i, frame_idx in enumerate(selected_indices):
                if frame_idx >= len(frame_ids) or frame_idx >= len(bboxes):
                    print(f"索引超出范围: frame_idx={frame_idx}, len(frame_ids)={len(frame_ids)}, len(bboxes)={len(bboxes)}")
                    continue
                
                # 获取帧ID和边界框
                target_frame_id = frame_ids[frame_idx]
                bbox = bboxes[frame_idx]
                
                print(f"尝试读取帧 {target_frame_id}, 边界框: {bbox}")
                
                # 检查帧ID是否在有效范围内
                if target_frame_id >= total_frames:
                    print(f"帧ID {target_frame_id} 超出视频总帧数 {total_frames}")
                    continue
                
                # 设置帧位置
                cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_id)
                ret, frame = cap.read()
                
                if ret:
                    print(f"成功读取帧 {target_frame_id}")
                    # Draw bounding boxes
                    processed_frame = self.draw_bbox(frame, bbox)
                    
                    # 转换为PIL图像
                    pil_image = Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
                    frames.append(pil_image)
                else:
                    print(f"无法读取帧 {target_frame_id}")
            
            cap.release()
            
            print(f"成功提取 {len(frames)} 帧")
            
            # 缓存结果
            self.cache[cache_key] = frames
            return frames
            
        except Exception as e:
            print(f"处理视频时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extract_frames_from_folder(self, folder_path: str, frame_ids: List[int], bboxes: List[List[float]], cache_key: str) -> List[Image.Image]:
        """
        从帧文件夹中读取帧图片（mtmmc场景）
        帧图片命名规则：000000.jpg, 000001.jpg, ...
        """
        try:
            print(f"从文件夹读取帧: {folder_path}")
            
            frames = []
            
            # 均匀选择3帧显示
            if len(frame_ids) > 3:
                step = len(frame_ids) // 3
                selected_indices = [0, step, len(frame_ids) - 1]
            else:
                selected_indices = list(range(len(frame_ids)))
            
            print(f"选择的帧索引: {selected_indices}")
            print(f"请求的帧ID: {frame_ids}")
            
            for i, frame_idx in enumerate(selected_indices):
                if frame_idx >= len(frame_ids) or frame_idx >= len(bboxes):
                    print(f"索引超出范围: frame_idx={frame_idx}, len(frame_ids)={len(frame_ids)}, len(bboxes)={len(bboxes)}")
                    continue
                
                # 获取帧ID和边界框
                target_frame_id = frame_ids[frame_idx]
                bbox = bboxes[frame_idx]
                
                # 构造帧图片文件名：000000.jpg格式
                frame_filename = f"{target_frame_id:06d}.jpg"
                frame_path = os.path.join(folder_path, frame_filename)
                
                print(f"尝试读取帧图片: {frame_path}, 边界框: {bbox}")
                
                if os.path.exists(frame_path):
                    try:
                        # 读取图片
                        frame = cv2.imread(frame_path)
                        if frame is not None:
                            print(f"成功读取帧图片 {frame_filename}")
                            # Draw bounding boxes
                            processed_frame = self.draw_bbox(frame, bbox)
                            
                            # 转换为PIL图像
                            pil_image = Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
                            frames.append(pil_image)
                        else:
                            print(f"无法读取帧图片: {frame_path}")
                    except Exception as e:
                        print(f"读取帧图片时出错: {str(e)}")
                else:
                    print(f"帧图片不存在: {frame_path}")
            
            print(f"成功提取 {len(frames)} 帧")
            
            # 缓存结果
            self.cache[cache_key] = frames
            return frames
            
        except Exception as e:
            print(f"从文件夹读取帧时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def draw_bbox(self, frame: np.ndarray, bbox: List[float]) -> np.ndarray:
        """
        在图像上绘制边界框
        
        Args:
            frame: 输入图像
            bbox: 边界框 [x, y, width, height]
            
        Returns:
            绘制了边界框的图像
        """
        if len(bbox) != 4:
            return frame
        
        x, y, w, h = map(int, bbox)
        
        # 确保坐标在图像范围内
        height, width = frame.shape[:2]
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        w = max(1, min(w, width - x))
        h = max(1, min(h, height - y))
        
        # Draw bounding boxes
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 添加标签
        label = "Target"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        
        # 计算文本大小
        (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        
        # 绘制文本背景
        cv2.rectangle(frame, (x, y - text_height - 10), (x + text_width, y), (0, 255, 0), -1)
        
        # 绘制文本
        cv2.putText(frame, label, (x, y - 5), font, font_scale, (0, 0, 0), thickness)
        
        return frame
    
    def extract_single_frame(self, video_path: str, frame_id: int) -> Optional[Image.Image]:
        """
        从视频或帧文件夹中提取单个帧
        
        Args:
            video_path: Video file path或帧文件夹路径
            frame_id: 帧ID
            
        Returns:
            提取的帧图像，如果失败则返回None
        """
        if not os.path.exists(video_path):
            return None
        
        # 判断是视频文件还是帧文件夹
        if os.path.isfile(video_path):
            # cityflow场景：从视频文件中提取帧
            return self._extract_single_frame_from_video(video_path, frame_id)
        elif os.path.isdir(video_path):
            # mtmmc场景：从帧文件夹中读取帧图片
            return self._extract_single_frame_from_folder(video_path, frame_id)
        else:
            return None
    
    def _extract_single_frame_from_video(self, video_path: str, frame_id: int) -> Optional[Image.Image]:
        """
        从视频文件中提取单个帧（cityflow场景）
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            return None
            
        except Exception as e:
            print(f"提取帧时出错: {str(e)}")
            return None
    
    def _extract_single_frame_from_folder(self, folder_path: str, frame_id: int) -> Optional[Image.Image]:
        """
        从帧文件夹中读取单个帧图片（mtmmc场景）
        """
        try:
            # 构造帧图片文件名：000000.jpg格式
            frame_filename = f"{frame_id:06d}.jpg"
            frame_path = os.path.join(folder_path, frame_filename)
            
            if os.path.exists(frame_path):
                # 读取图片
                frame = cv2.imread(frame_path)
                if frame is not None:
                    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            return None
            
        except Exception as e:
            print(f"从文件夹读取帧时出错: {str(e)}")
            return None
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        获取视频信息
        
        Args:
            video_path: Video file path
            
        Returns:
            视频信息字典
        """
        if not os.path.exists(video_path):
            return None
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None
            
            info = {
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
            }
            
            cap.release()
            return info
            
        except Exception as e:
            print(f"获取视频信息时出错: {str(e)}")
            return None
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
    
    def get_cache_size(self) -> int:
        """获取缓存大小"""
        return len(self.cache)
