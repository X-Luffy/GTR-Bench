#!/usr/bin/env python3
"""
根据case_id匹配，从原始备份文件中恢复video_path和crop_video_path字段
"""

import json
import os
import glob

def restore_paths_from_backup():
    # 当前数据目录
    current_data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    # 备份数据目录
    backup_data_dir = "/home/mnt/xieqinghongbing/data/question_generation/benchmark/selected"
    
    # 处理cityflow场景
    print("处理cityflow场景...")
    current_cityflow_dir = os.path.join(current_data_dir, "cityflow")
    backup_cityflow_dir = os.path.join(backup_data_dir, "cityflow")
    
    current_cityflow_files = glob.glob(os.path.join(current_cityflow_dir, "*.json"))
    
    for current_file in current_cityflow_files:
        filename = os.path.basename(current_file)
        backup_file = os.path.join(backup_cityflow_dir, filename)
        
        if not os.path.exists(backup_file):
            print(f"  警告: 备份文件不存在: {backup_file}")
            continue
            
        print(f"  处理文件: {filename}")
        
        # 读取当前文件
        with open(current_file, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        
        # 读取备份文件
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # 创建备份数据的case_id映射
        backup_cases = {}
        if 'cases' in backup_data:
            for case in backup_data['cases']:
                case_id = case.get('case_id')
                if case_id:
                    backup_cases[case_id] = case
        
        # 恢复路径
        restored_count = 0
        if 'cases' in current_data:
            for case in current_data['cases']:
                case_id = case.get('case_id')
                if case_id and case_id in backup_cases:
                    backup_case = backup_cases[case_id]
                    
                    # 恢复camera_images中的路径
                    if 'camera_images' in case and 'camera_images' in backup_case:
                        current_cameras = case['camera_images']
                        backup_cameras = backup_case['camera_images']
                        
                        # 根据camera_id匹配
                        backup_camera_map = {}
                        for cam in backup_cameras:
                            camera_id = cam.get('camera_id')
                            if camera_id:
                                backup_camera_map[camera_id] = cam
                        
                        for current_cam in current_cameras:
                            camera_id = current_cam.get('camera_id')
                            if camera_id and camera_id in backup_camera_map:
                                backup_cam = backup_camera_map[camera_id]
                                
                                # 恢复video_path
                                if 'video_path' in backup_cam:
                                    current_cam['video_path'] = backup_cam['video_path']
                                    restored_count += 1
                                
                                # 恢复crop_video_path
                                if 'crop_video_path' in backup_cam:
                                    current_cam['crop_video_path'] = backup_cam['crop_video_path']
                                    restored_count += 1
        
        if restored_count > 0:
            # 保存修改后的文件
            with open(current_file, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            print(f"    恢复了 {restored_count} 个路径字段")
        else:
            print(f"    没有找到匹配的case_id")
    
    # 处理mtmmc场景
    print("\n处理mtmmc场景...")
    current_mtmmc_dir = os.path.join(current_data_dir, "mtmmc")
    backup_mtmmc_dir = os.path.join(backup_data_dir, "mtmmc")
    
    current_mtmmc_files = glob.glob(os.path.join(current_mtmmc_dir, "*.json"))
    
    for current_file in current_mtmmc_files:
        filename = os.path.basename(current_file)
        backup_file = os.path.join(backup_mtmmc_dir, filename)
        
        if not os.path.exists(backup_file):
            print(f"  警告: 备份文件不存在: {backup_file}")
            continue
            
        print(f"  处理文件: {filename}")
        
        # 读取当前文件
        with open(current_file, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        
        # 读取备份文件
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # 创建备份数据的case_id映射
        backup_cases = {}
        if 'cases' in backup_data:
            for case in backup_data['cases']:
                case_id = case.get('case_id')
                if case_id:
                    backup_cases[case_id] = case
        
        # 恢复路径
        restored_count = 0
        if 'cases' in current_data:
            for case in current_data['cases']:
                case_id = case.get('case_id')
                if case_id and case_id in backup_cases:
                    backup_case = backup_cases[case_id]
                    
                    # 恢复camera_images中的路径
                    if 'camera_images' in case and 'camera_images' in backup_case:
                        current_cameras = case['camera_images']
                        backup_cameras = backup_case['camera_images']
                        
                        # 根据camera_id匹配
                        backup_camera_map = {}
                        for cam in backup_cameras:
                            camera_id = cam.get('camera_id')
                            if camera_id:
                                backup_camera_map[camera_id] = cam
                        
                        for current_cam in current_cameras:
                            camera_id = current_cam.get('camera_id')
                            if camera_id and camera_id in backup_camera_map:
                                backup_cam = backup_camera_map[camera_id]
                                
                                # 恢复video_path
                                if 'video_path' in backup_cam:
                                    current_cam['video_path'] = backup_cam['video_path']
                                    restored_count += 1
                                
                                # 恢复crop_video_path
                                if 'crop_video_path' in backup_cam:
                                    current_cam['crop_video_path'] = backup_cam['crop_video_path']
                                    restored_count += 1
        
        if restored_count > 0:
            # 保存修改后的文件
            with open(current_file, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            print(f"    恢复了 {restored_count} 个路径字段")
        else:
            print(f"    没有找到匹配的case_id")
    
    print("\n✓ 路径恢复完成!")

if __name__ == "__main__":
    restore_paths_from_backup()
