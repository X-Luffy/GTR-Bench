#!/usr/bin/env python3
"""
处理JSON文件中的视频路径，复制文件并更新为相对路径
同时删除choices_cn字段
"""

import json
import os
import shutil
import re
from pathlib import Path
import glob
import sys

def extract_filename_from_path(path, scene_type):
    """
    根据路径提取新的文件名
    """
    if scene_type == "cityflow":
        # cityflow video_path: /home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/train/S04/c021/vdo.avi
        # 新名字: cityflow_S04_c021.avi
        if "train/" in path:
            match = re.search(r'/train/([^/]+)/([^/]+)/', path)
            if match:
                scene, camera = match.groups()
                ext = os.path.splitext(path)[1]
                return f"cityflow_{scene}_{camera}{ext}"
        
        # cityflow video_path: /home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/validation/S05/c026/vdo.avi
        # 新名字: cityflow_S05_c026.avi
        elif "validation/" in path:
            match = re.search(r'/validation/([^/]+)/([^/]+)/', path)
            if match:
                scene, camera = match.groups()
                ext = os.path.splitext(path)[1]
                return f"cityflow_{scene}_{camera}{ext}"
        
        # cityflow crop_video_path: /home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/track_processed/S04/259/video/43_56_c021.mp4
        # 新名字: cityflow_S04_259_43_59_c021.mp4
        elif "track_processed/" in path:
            match = re.search(r'/track_processed/([^/]+)/([^/]+)/video/([^/]+)', path)
            if match:
                scene, obj_id, filename = match.groups()
                return f"cityflow_{scene}_{obj_id}_{filename}"
    
    elif scene_type == "mtmmc":
        # mtmmc video_path: /home/mnt/xieqinghongbing/data/mtmmc/train/s01/c04/rgb (目录)
        # 新名字: mtmmc_s01_c04 (目录名)
        if "/train/" in path and path.endswith("/rgb"):
            match = re.search(r'/train/([^/]+)/([^/]+)/rgb', path)
            if match:
                scene, camera = match.groups()
                return f"mtmmc_{scene}_{camera}"
        
        # mtmmc crop_video_path: /home/mnt/xieqinghongbing/data/mtmmc/train/../track_processed/s01/4/video_vis/39_50_c03.mp4
        # 新名字: mtmmc_s01_4_39_50_c03.mp4
        elif "track_processed/" in path:
            match = re.search(r'/track_processed/([^/]+)/([^/]+)/video_vis/([^/]+)', path)
            if match:
                scene, obj_id, filename = match.groups()
                return f"mtmmc_{scene}_{obj_id}_{filename}"
    
    # 如果无法解析，使用原文件名
    return os.path.basename(path)

def copy_video_file(src_path, dst_path, scene_type):
    """
    复制视频文件或目录
    """
    if not os.path.exists(src_path):
        print(f"警告: 源文件不存在: {src_path}")
        return False
    
    # 检查目标文件是否已存在
    if os.path.exists(dst_path):
        print(f"文件已存在，跳过复制: {dst_path}")
        return True
    
    try:
        if os.path.isdir(src_path):
            # 对于mtmmc的rgb目录，复制整个目录
            shutil.copytree(src_path, dst_path)
            print(f"复制目录: {src_path} -> {dst_path}")
        else:
            # 复制单个文件
            shutil.copy2(src_path, dst_path)
            print(f"复制文件: {src_path} -> {dst_path}")
        return True
    except Exception as e:
        print(f"复制失败: {src_path} -> {dst_path}, 错误: {e}")
        return False

def process_json_file(json_path, scene_type):
    """
    处理单个JSON文件
    """
    print(f"\n开始处理文件: {json_path}")
    
    # 读取JSON文件
    print("  读取JSON文件...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 确定目标目录
    base_dir = os.path.dirname(json_path)
    raw_video_dir = os.path.join(base_dir, "raw_video")
    crop_video_dir = os.path.join(base_dir, "crop_video")
    
    # 统计需要处理的文件数量
    total_files = 0
    if 'cases' in data:
        for case in data['cases']:
            if 'camera_images' in case:
                for camera_image in case['camera_images']:
                    if 'video_path' in camera_image and camera_image['video_path'] and camera_image['video_path'].startswith('/'):
                        total_files += 1
                    if 'crop_video_path' in camera_image and camera_image['crop_video_path'] and camera_image['crop_video_path'].startswith('/'):
                        total_files += 1
    
    print(f"  需要处理 {total_files} 个文件")
    
    # 处理cases中的每个case
    processed_files = 0
    if 'cases' in data:
        for case_idx, case in enumerate(data['cases']):
            if 'camera_images' in case:
                for camera_image in case['camera_images']:
                    # 处理video_path
                    if 'video_path' in camera_image:
                        src_path = camera_image['video_path']
                        if src_path and src_path.startswith('/'):
                            new_filename = extract_filename_from_path(src_path, scene_type)
                            
                            if scene_type == "mtmmc" and os.path.isdir(src_path):
                                # mtmmc的video_path是目录
                                dst_path = os.path.join(raw_video_dir, new_filename)
                                if copy_video_file(src_path, dst_path, scene_type):
                                    camera_image['video_path'] = f"./raw_video/{new_filename}"
                            else:
                                # cityflow的video_path是文件
                                dst_path = os.path.join(raw_video_dir, new_filename)
                                if copy_video_file(src_path, dst_path, scene_type):
                                    camera_image['video_path'] = f"./raw_video/{new_filename}"
                            processed_files += 1
                            if processed_files % 10 == 0:
                                print(f"    已处理 {processed_files}/{total_files} 个文件")
                    
                    # 处理crop_video_path
                    if 'crop_video_path' in camera_image:
                        src_path = camera_image['crop_video_path']
                        if src_path and src_path.startswith('/'):
                            new_filename = extract_filename_from_path(src_path, scene_type)
                            dst_path = os.path.join(crop_video_dir, new_filename)
                            if copy_video_file(src_path, dst_path, scene_type):
                                camera_image['crop_video_path'] = f"./crop_video/{new_filename}"
                            processed_files += 1
                            if processed_files % 10 == 0:
                                print(f"    已处理 {processed_files}/{total_files} 个文件")
    
    print(f"  文件复制完成，共处理 {processed_files} 个文件")
    
    # 删除choices_cn字段
    print("  删除choices_cn字段...")
    def remove_choices_cn(obj):
        if isinstance(obj, dict):
            if 'choices_cn' in obj:
                del obj['choices_cn']
            for value in obj.values():
                remove_choices_cn(value)
        elif isinstance(obj, list):
            for item in obj:
                remove_choices_cn(item)
    
    remove_choices_cn(data)
    
    # 写回JSON文件
    print("  保存JSON文件...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 完成处理: {json_path}")

def main():
    """
    主函数
    """
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    print("=" * 60)
    print("开始处理数据集文件...")
    print("=" * 60)
    
    # 处理cityflow场景
    cityflow_dir = os.path.join(data_dir, "cityflow")
    cityflow_json_files = glob.glob(os.path.join(cityflow_dir, "*.json"))
    
    print(f"\n处理cityflow场景，共 {len(cityflow_json_files)} 个JSON文件...")
    for i, json_file in enumerate(cityflow_json_files, 1):
        print(f"\n[{i}/{len(cityflow_json_files)}] 处理cityflow文件...")
        process_json_file(json_file, "cityflow")
    
    # 处理mtmmc场景
    mtmmc_dir = os.path.join(data_dir, "mtmmc")
    mtmmc_json_files = glob.glob(os.path.join(mtmmc_dir, "*.json"))
    
    print(f"\n处理mtmmc场景，共 {len(mtmmc_json_files)} 个JSON文件...")
    for i, json_file in enumerate(mtmmc_json_files, 1):
        print(f"\n[{i}/{len(mtmmc_json_files)}] 处理mtmmc文件...")
        process_json_file(json_file, "mtmmc")
    
    print("\n" + "=" * 60)
    print("✓ 所有文件处理完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
