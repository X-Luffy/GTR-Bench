#!/usr/bin/env python3
"""
修复错误的相对路径，将./raw_video/vdo.avi替换为正确的路径
"""

import json
import os
import glob
import re

def fix_wrong_relative_paths():
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    # 处理cityflow文件
    cityflow_dir = os.path.join(data_dir, "cityflow")
    cityflow_json_files = glob.glob(os.path.join(cityflow_dir, "*.json"))
    
    for json_file in cityflow_json_files:
        print(f"处理文件: {json_file}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed_count = 0
        
        if 'cases' in data:
            for case in data['cases']:
                scene = case.get('scene', '')
                if 'camera_images' in case:
                    for camera_image in case['camera_images']:
                        camera_id = camera_image.get('camera_id', '')
                        
                        # 修复错误的video_path
                        if 'video_path' in camera_image:
                            video_path = camera_image['video_path']
                            if video_path == "./raw_video/vdo.avi":
                                # 从crop_video_path中提取正确的camera信息
                                correct_camera = None
                                if 'crop_video_path' in camera_image:
                                    crop_path = camera_image['crop_video_path']
                                    # 从crop_video_path中提取camera_id，格式如：cityflow_S05_354_213_224_c026.mp4
                                    match = re.search(r'_c(\d+)\.mp4$', crop_path)
                                    if match:
                                        correct_camera = f"c{match.group(1)}"
                                
                                # 使用正确的camera_id
                                if scene and correct_camera:
                                    # 检查validation路径
                                    validation_path = f"/home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/validation/{scene}/{correct_camera}/vdo.avi"
                                    if os.path.exists(validation_path):
                                        new_filename = f"cityflow_{scene}_{correct_camera}.avi"
                                        new_path = f"./raw_video/{new_filename}"
                                        
                                        # 更新路径
                                        camera_image['video_path'] = new_path
                                        fixed_count += 1
                                        print(f"  修复路径: {video_path} -> {new_path} (从camera_id {camera_id} 修正为 {correct_camera})")
                                        
                                        # 复制文件（如果目标文件不存在）
                                        target_path = os.path.join(os.path.dirname(json_file), "raw_video", new_filename)
                                        if not os.path.exists(target_path):
                                            import shutil
                                            shutil.copy2(validation_path, target_path)
                                            print(f"  复制文件: {validation_path} -> {target_path}")
        
        if fixed_count > 0:
            # 保存修改后的文件
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  修复了 {fixed_count} 个路径，已保存文件")
        else:
            print("  没有需要修复的路径")

if __name__ == "__main__":
    fix_wrong_relative_paths()
