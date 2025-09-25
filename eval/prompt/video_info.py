import os
import glob
import cv2
from utils.time_utils import convert_seconds_to_timecode
from utils.image_utils import load_image, image_to_base64
from PIL import Image, ImageDraw, ImageFont


def prompt_cam_desc_en(cam_data, with_direction, with_timestamp, with_bbox):
    # Convert timestamp to HH:MM:SS.sss format
    start_timestamp_sec = float(cam_data['start_timestamp'])
    end_timestamp_sec = float(cam_data['end_timestamp'])
    start_timestamp_str = convert_seconds_to_timecode(start_timestamp_sec)
    end_timestamp_str = convert_seconds_to_timecode(end_timestamp_sec)
    
    # Modify camera description using formatted time and adding target ID
    camera_desc = f"""Camera {cam_data['camera_id']} """
    if with_direction:
        camera_desc += f"""Direction: {cam_data.get('direction', 'Unknown direction')} \n"""
    if with_timestamp:
        camera_desc += f"""Time period {start_timestamp_str}-{end_timestamp_str} \n"""
    
    if with_bbox:
        # Add detailed bounding box information (with timestamps)
        bbox_info = f"Bounding box details for target ID: {cam_data['object_id']}:\n"
        frame_count = len(cam_data['bboxes'])
        
        # Calculate time interval between frames (assuming uniform distribution)
        if frame_count > 1:
            time_step = (end_timestamp_sec - start_timestamp_sec) / (frame_count - 1)
        else:
            time_step = 0
        
    camera_desc += f"capturing target ID: {cam_data['object_id']}"
    
    for i, box in enumerate(cam_data['bboxes']):
        if i < len(cam_data['images']):
            # Calculate timestamp for this frame
            frame_timestamp = start_timestamp_sec + (i * time_step)
            time_str = convert_seconds_to_timecode(frame_timestamp)
            if with_timestamp:
                bbox_info += f"Frame {i+1}: [x={box[0]:.1f}, y={box[1]:.1f}, w={box[2]:.1f}, h={box[3]:.1f}], Time: {time_str}\n"
            else:
                bbox_info += f"Frame {i+1}: [x={box[0]:.1f}, y={box[1]:.1f}, w={box[2]:.1f}, h={box[3]:.1f}]\n"
    
    # Adjust corner information description based on with_timestamp parameter
    if with_timestamp:
        corner_info_desc = "Top-right corner of image contains target task ID, timestamp and bounding box information"
    else:
        corner_info_desc = "Top-right corner of image contains target task ID and bounding box information"
    TEMP = """Red box marks the target person (ID: {obj_id}), box format is [x, y, width, height]
{corner_info_desc}
{bbox_info}
"""
    camera_desc += TEMP.format(
        obj_id=cam_data['object_id'],
        corner_info_desc=corner_info_desc,
        bbox_info=bbox_info
    )

    return camera_desc

def make_keyframe_prompt(case,with_timestamp=True,with_direction=True,
        with_bbox=True,is_random=False,
        is_resize=False,frame_limited=3):
    messages = []
    # 收集摄像头图像和处理bounding box信息
    camera_data = []
    
    for camera_item in case.get("camera_images", []):
        camera_id = camera_item.get("camera_id", "")
        object_id = camera_item.get("object_id", "")
        keyframes_path = camera_item.get("keyframes_path", "")
        video_path = camera_item.get("video_path", "")
        frame_ids = camera_item.get("frame_ids", [])
        bboxes = camera_item.get("bboxes", [])
        start_timestamp = camera_item.get("start_timestamp", "")
        end_timestamp = camera_item.get("end_timestamp", "")
        
        # 转换时间戳为数值
        start_timestamp_sec = float(start_timestamp)
        end_timestamp_sec = float(end_timestamp)
        
        # 加载关键帧图像
        keyframe_images = []
        
        # 优先尝试从视频文件加载帧
        if video_path and os.path.exists(video_path) and frame_ids and bboxes:
            print(f"从视频文件加载关键帧: {video_path}")
            keyframe_data = load_keyframes_from_video(
                video_path, frame_ids, bboxes, object_id, 
                start_timestamp_sec, end_timestamp_sec, with_timestamp,with_bbox
            )
            keyframe_images = [img for _, img in keyframe_data]
        
        # 如果视频加载失败，回退到原有的图片目录加载方式
        if not keyframe_images and keyframes_path and os.path.exists(keyframes_path):
            print(f"回退到图片目录加载: {keyframes_path}")
            for img_file in sorted(os.listdir(keyframes_path)):
                if img_file.endswith(('.jpg', '.png')):
                    img_path = os.path.join(keyframes_path, img_file)
                    img = load_image(img_path)
                    if img:
                        keyframe_images.append(img)
        
        # 如果关键帧目录不存在或为空，尝试使用frame_ids直接加载
        if not keyframe_images and keyframes_path:
            keyframe_data = load_keyframe_images(keyframes_path, frame_ids)
            keyframe_images = [img for _, img in keyframe_data]

        # 创建摄像头数据对象
        camera_data.append({
            "camera_id": camera_id,
            "object_id": object_id,
            "images": keyframe_images,
            "bboxes": bboxes,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp
        })
    
    if frame_limited != 0:
        for cam_data in camera_data:
            # 限制每个摄像头的图像数量
            if len(cam_data['images']) > frame_limited:
                inverval = len(cam_data['images']) // frame_limited
                cam_data['images'] = cam_data['images'][::inverval]
                cam_data['bboxes'] = cam_data['bboxes'][::inverval]

    if is_random:
        # 随机打乱摄像头数据顺序
        import random
        random.shuffle(camera_data)

    for cam_data in camera_data:
        
        camera_desc = prompt_cam_desc_en(cam_data,with_direction=with_direction,
        with_timestamp=with_timestamp,with_bbox=with_bbox)
        
        messages.append({
            'type': 'text',
            'text': camera_desc
        })
        

        # 添加图像
        for img in cam_data['images']:
            if is_resize:
                width, height  = img.size
                aspect_ratio = width / height
                # 将图像调整为512高度，保持宽高比
                new_height = 512
                new_width = int(new_height * aspect_ratio)
                img = img.resize((new_width, new_height))  # 保持原有比例
            messages.append({
                'type': 'image_url',
                'image_url': {
                    'url': image_to_base64(img),
                }
            })
    return messages

def load_keyframe_images(keyframes_path, frame_ids, max_images=9):
    """加载关键帧图像"""
    loaded_images = []
    
    # 确保关键帧路径存在
    if not os.path.exists(keyframes_path):
        print(f"关键帧路径不存在: {keyframes_path}")
        return loaded_images
    
    # 获取关键帧目录中的所有图像文件
    image_files = glob.glob(os.path.join(keyframes_path, "*.jpg")) + glob.glob(os.path.join(keyframes_path, "*.png"))
    
    # 确保只处理指定的frame_ids对应的图像
    for i, frame_id in enumerate(frame_ids):
        if i >= max_images:  # 限制最大图像数量
            break
            
        # 尝试不同的文件名格式
        possible_paths = [
            os.path.join(keyframes_path, f"{frame_id}.jpg"),
            os.path.join(keyframes_path, f"{frame_id}.png"),
            os.path.join(keyframes_path, f"frame_{frame_id}.jpg"),
            os.path.join(keyframes_path, f"frame_{frame_id}.png")
        ]
        
        image_loaded = False
        for path in possible_paths:
            if path in image_files or os.path.exists(path):
                img = load_image(path)
                if img:
                    loaded_images.append((frame_id, img))
                    image_loaded = True
                    break
        
        if not image_loaded:
            print(f"未找到frame_id为{frame_id}的图像")
    
    return loaded_images

def load_keyframes_from_video(video_path, frame_ids, bboxes, object_id, start_timestamp_sec, end_timestamp_sec,with_timestamp=True, with_bbox=True):
    """从视频中加载关键帧并绘制边界框"""
    loaded_images = []
    
    if not os.path.exists(video_path):
        print(f"视频文件不存在: {video_path}")
        return loaded_images
    
    # 计算帧之间的时间间隔（假设均匀分布）
    frame_count = len(frame_ids)
    if frame_count > 1:
        time_step = (end_timestamp_sec - start_timestamp_sec) / (frame_count - 1)
    else:
        time_step = 0
    
    # 选择三张均匀分布的图片
    selected_indices = []
    if frame_count <= 3:
        # 如果总帧数不超过3张，全部选择
        selected_indices = list(range(frame_count))
    else:
        # 选择三张均匀分布的图片：开始、中间、结束
        selected_indices = [0, frame_count // 2, frame_count - 1]
    
    for i in selected_indices:
        if i >= len(frame_ids) or i >= len(bboxes):
            print(f"警告: 索引 {i} 超出范围")
            continue
            
        frame_id = frame_ids[i]
        bbox = bboxes[i]

        if video_path.endswith('.mp4') or video_path.endswith('.avi'):
            # 从视频中抽取帧
            frame_image = extract_frame_from_video(video_path, frame_id)
        else:            # 如果不是视频文件，尝试直接加载图像
            frame_image = load_image(os.path.join(video_path, f"{frame_id:06d}.jpg"))#000020

        if frame_image is None:
            continue
            
        # 计算该帧的时间戳
        frame_timestamp = start_timestamp_sec + (i * time_step)
        timestamp_str = convert_seconds_to_timecode(frame_timestamp)
        
        # 在图像上绘制边界框
        img_with_bbox = draw_bbox_on_image(frame_image, bbox, object_id, frame_id, timestamp_str, with_bbox=with_bbox, with_timestamp=with_timestamp)
        
        loaded_images.append((frame_id, img_with_bbox))
        print(f"成功加载并处理frame {frame_id}")
    
    return loaded_images

def draw_bbox_on_image(image, bbox, object_id, frame_id, timestamp_str, with_bbox=True, with_timestamp=True):
    """在图像上绘制边界框和信息"""
    try:
        # 创建图像副本用于绘制
        img_with_bbox = image.copy()
        draw = ImageDraw.Draw(img_with_bbox)
        
        # 解析bbox [x, y, width, height]
        x, y, w, h = bbox
        
        # 绘制红色边界框
        draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
        
        # 在图像右上角添加信息文本
        info_text = f"ID:{object_id} \n"
        
        if with_timestamp:
            info_text += f"Frame:{frame_id} Time:{timestamp_str} \n"
        if with_bbox:
            info_text += f"Box:[{x:.1f},{y:.1f},{w:.1f},{h:.1f}] \n"

        # 获取图像尺寸
        img_width, img_height = img_with_bbox.size
        
        # 在右上角绘制背景矩形
        text_lines = info_text.split('\n')
        max_line_length = max(len(line) for line in text_lines)
        text_height = len(text_lines) * 20   # 增加行高
        text_width = max_line_length * 10    # 增加字符宽度
        
        # 绘制半透明背景
        background_coords = [img_width - text_width, 0, img_width, text_height]
        draw.rectangle(background_coords, fill=(0, 0, 0, 180))
        draw.rectangle(background_coords, outline="white", width=2)
        
        from PIL import ImageFont

        # 创建字体对象，指定大小
        try:
            # 尝试加载自定义字体
            font_path = os.path.join(os.path.dirname(__file__), "..", "utils", "ARIAL.TTF")
            font = ImageFont.truetype(font_path, size=18)
        except Exception as e:
            # 如果加载失败，使用默认字体
            print(f"字体加载失败，使用默认字体: {str(e)}")
            font = ImageFont.load_default()

        
        y_offset = 8
        for line in text_lines:
            draw.text((img_width - text_width + 8, y_offset), line, fill="white",font=font)
            y_offset += 20
        
        return img_with_bbox
        
    except Exception as e:
        print(f"绘制边界框失败: {str(e)}")
        return image

def extract_frame_from_video(video_path, frame_id):
    """从视频中抽取指定帧"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return None
        
        # 设置到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # 转换BGR到RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转换为PIL图像
            pil_image = Image.fromarray(frame_rgb)
            return pil_image
        else:
            print(f"无法读取视频帧 {frame_id} from {video_path}")
            return None
            
    except Exception as e:
        print(f"从视频抽取帧失败: {str(e)}")
        return None