#!/usr/bin/env python3
"""
1. 重命名文件：cityflow/mtmmc -> outdoor/indoor
2. 重命名任务：MotionReasoning->MotionState, TemporalReasoning->ArrivalTimeInterval, 等
3. 更新JSON中的task_id和map_image_path
4. 删除指定字段
"""

import json
import os
import shutil
import glob
import re

# 任务名称映射
TASK_MAPPING = {
    "MotionReasoning": "MotionState",
    "TemporalReasoning": "ArrivalTimeInterval", 
    "SpatialReasoning": "GeoLocation",
    "TimelineInference": "CasualReordering",
    "NextCameraForecasting": "NextSpotForecasting"
}

# 场景名称映射
SCENE_MAPPING = {
    "cityflow": "outdoor",
    "mtmmc": "indoor"
}

def rename_files_and_directories():
    """重命名文件和目录"""
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    # 重命名场景目录
    for old_scene, new_scene in SCENE_MAPPING.items():
        old_dir = os.path.join(data_dir, old_scene)
        new_dir = os.path.join(data_dir, new_scene)
        
        if os.path.exists(old_dir) and not os.path.exists(new_dir):
            shutil.move(old_dir, new_dir)
            print(f"重命名目录: {old_scene} -> {new_scene}")
    
    # 重命名raw_video和crop_video中的文件
    for old_scene, new_scene in SCENE_MAPPING.items():
        new_dir = os.path.join(data_dir, new_scene)
        if os.path.exists(new_dir):
            # 重命名raw_video中的文件
            raw_video_dir = os.path.join(new_dir, "raw_video")
            if os.path.exists(raw_video_dir):
                for filename in os.listdir(raw_video_dir):
                    if filename.startswith(old_scene):
                        old_path = os.path.join(raw_video_dir, filename)
                        new_filename = filename.replace(old_scene, new_scene, 1)
                        new_path = os.path.join(raw_video_dir, new_filename)
                        shutil.move(old_path, new_path)
                        print(f"重命名文件: {filename} -> {new_filename}")
            
            # 重命名crop_video中的文件
            crop_video_dir = os.path.join(new_dir, "crop_video")
            if os.path.exists(crop_video_dir):
                for filename in os.listdir(crop_video_dir):
                    if filename.startswith(old_scene):
                        old_path = os.path.join(crop_video_dir, filename)
                        new_filename = filename.replace(old_scene, new_scene, 1)
                        new_path = os.path.join(crop_video_dir, new_filename)
                        shutil.move(old_path, new_path)
                        print(f"重命名文件: {filename} -> {new_filename}")

def rename_json_files():
    """重命名JSON文件"""
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    for old_scene, new_scene in SCENE_MAPPING.items():
        scene_dir = os.path.join(data_dir, new_scene)
        if os.path.exists(scene_dir):
            json_files = glob.glob(os.path.join(scene_dir, "*.json"))
            
            for json_file in json_files:
                filename = os.path.basename(json_file)
                
                # 重命名场景前缀
                if filename.startswith(old_scene):
                    new_filename = filename.replace(old_scene, new_scene, 1)
                    new_path = os.path.join(scene_dir, new_filename)
                    shutil.move(json_file, new_path)
                    print(f"重命名JSON文件: {filename} -> {new_filename}")
                    json_file = new_path
                
                # 重命名任务名称
                for old_task, new_task in TASK_MAPPING.items():
                    if old_task in filename:
                        new_filename = filename.replace(old_task, new_task)
                        new_path = os.path.join(scene_dir, new_filename)
                        shutil.move(json_file, new_path)
                        print(f"重命名JSON文件: {os.path.basename(json_file)} -> {new_filename}")
                        json_file = new_path
                        break

def rename_media_files():
    """重命名media文件并移动到map目录"""
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    for old_scene, new_scene in SCENE_MAPPING.items():
        scene_dir = os.path.join(data_dir, new_scene)
        if os.path.exists(scene_dir):
            media_dir = os.path.join(scene_dir, "media")
            map_dir = os.path.join(scene_dir, "map")
            
            if os.path.exists(media_dir):
                # 创建map目录
                if not os.path.exists(map_dir):
                    os.makedirs(map_dir)
                
                # 重命名并移动文件
                for filename in os.listdir(media_dir):
                    if filename.endswith('.png'):
                        old_path = os.path.join(media_dir, filename)
                        
                        # 更新文件名中的任务名称
                        new_filename = filename
                        for old_task, new_task in TASK_MAPPING.items():
                            if old_task in filename:
                                new_filename = new_filename.replace(old_task, new_task)
                                break
                        
                        new_path = os.path.join(map_dir, new_filename)
                        shutil.move(old_path, new_path)
                        print(f"移动并重命名文件: {filename} -> {new_filename}")
                
                # 删除空的media目录
                if not os.listdir(media_dir):
                    os.rmdir(media_dir)
                    print(f"删除空目录: {media_dir}")

def update_json_content():
    """更新JSON文件内容"""
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    for old_scene, new_scene in SCENE_MAPPING.items():
        scene_dir = os.path.join(data_dir, new_scene)
        if os.path.exists(scene_dir):
            json_files = glob.glob(os.path.join(scene_dir, "*.json"))
            
            for json_file in json_files:
                print(f"处理JSON文件: {json_file}")
                
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 更新task_id
                if 'cases' in data:
                    for case in data['cases']:
                        if 'task_id' in case:
                            old_task_id = case['task_id']
                            for old_task, new_task in TASK_MAPPING.items():
                                if old_task in old_task_id:
                                    case['task_id'] = old_task_id.replace(old_task, new_task)
                                    break
                        
                        # 更新map_image_path
                        if 'map_image_path' in case:
                            old_path = case['map_image_path']
                            if old_path.startswith('./media/'):
                                # 提取文件名部分
                                filename = os.path.basename(old_path)
                                
                                # 更新任务名称
                                new_filename = filename
                                for old_task, new_task in TASK_MAPPING.items():
                                    if old_task in filename:
                                        new_filename = new_filename.replace(old_task, new_task)
                                        break
                                
                                # 更新路径
                                case['map_image_path'] = f"./map/{new_filename}"
                        
                        # 更新camera_images中的路径
                        if 'camera_images' in case:
                            for camera_image in case['camera_images']:
                                # 更新video_path
                                if 'video_path' in camera_image:
                                    old_path = camera_image['video_path']
                                    if old_scene in old_path:
                                        new_path = old_path.replace(old_scene, new_scene)
                                        camera_image['video_path'] = new_path
                                
                                # 更新crop_video_path
                                if 'crop_video_path' in camera_image:
                                    old_path = camera_image['crop_video_path']
                                    if old_scene in old_path:
                                        new_path = old_path.replace(old_scene, new_scene)
                                        camera_image['crop_video_path'] = new_path
                        
                        # 删除指定字段
                        fields_to_remove = ['question_type', 'target_event', 'related_events', 'reasoning_chain']
                        for field in fields_to_remove:
                            if field in case:
                                del case[field]
                
                # 保存修改后的文件
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"  更新完成")

def main():
    """主函数"""
    print("=" * 60)
    print("开始重命名和清理任务...")
    print("=" * 60)
    
    print("\n1. 重命名文件和目录...")
    rename_files_and_directories()
    
    print("\n2. 重命名JSON文件...")
    rename_json_files()
    
    print("\n3. 重命名media文件并移动到map目录...")
    rename_media_files()
    
    print("\n4. 更新JSON文件内容...")
    update_json_content()
    
    print("\n" + "=" * 60)
    print("✓ 所有任务完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
