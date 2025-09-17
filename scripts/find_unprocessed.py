#!/usr/bin/env python3
import json
import os
import glob

def find_unprocessed_paths():
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    # 检查cityflow文件
    cityflow_dir = os.path.join(data_dir, "cityflow")
    cityflow_json_files = glob.glob(os.path.join(cityflow_dir, "*.json"))
    
    for json_file in cityflow_json_files:
        print(f"\n检查文件: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'cases' in data:
            for case_idx, case in enumerate(data['cases']):
                if 'camera_images' in case:
                    for cam_idx, camera_image in enumerate(case['camera_images']):
                        # 检查video_path
                        if 'video_path' in camera_image:
                            video_path = camera_image['video_path']
                            if video_path and video_path.startswith('/'):
                                print(f"  未处理的video_path: {video_path}")
                            elif video_path == "./raw_video/vdo.avi":
                                print(f"  可疑的video_path: {video_path} (case {case_idx}, camera {cam_idx})")
                        
                        # 检查crop_video_path
                        if 'crop_video_path' in camera_image:
                            crop_path = camera_image['crop_video_path']
                            if crop_path and crop_path.startswith('/'):
                                print(f"  未处理的crop_video_path: {crop_path}")

if __name__ == "__main__":
    find_unprocessed_paths()
