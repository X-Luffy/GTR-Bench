#!/usr/bin/env python3
"""
修复错误的video_path，根据camera_id和scene信息推断正确的原始路径
"""

import json
import os
import glob

def fix_incorrect_paths():
    data_dir = "/home/mnt/xieqinghongbing/code/xiazhaoyuan/paper/human_level/data"
    
    # 处理cityflow文件
    cityflow_dir = os.path.join(data_dir, "cityflow")
    cityflow_json_files = glob.glob(os.path.join(cityflow_dir, "*.json"))
    
    for json_file in cityflow_json_files:
        print(f"\n处理文件: {json_file}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed_count = 0
        
        if 'cases' in data:
            for case_idx, case in enumerate(data['cases']):
                scene = case.get('scene', '')
                if 'camera_images' in case:
                    for cam_idx, camera_image in enumerate(case['camera_images']):
                        camera_id = camera_image.get('camera_id', '')
                        
                        # 检查并修复错误的video_path
                        if 'video_path' in camera_image:
                            video_path = camera_image['video_path']
                            if video_path == "./raw_video/vdo.avi":
                                # 根据scene和camera_id推断正确的路径
                                if scene and camera_id:
                                    # 检查原始文件是否存在
                                    original_path = f"/home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/train/{scene}/{camera_id}/vdo.avi"
                                    if os.path.exists(original_path):
                                        # 生成正确的新文件名
                                        new_filename = f"cityflow_{scene}_{camera_id}.avi"
                                        new_path = f"./raw_video/{new_filename}"
                                        
                                        # 更新路径
                                        camera_image['video_path'] = new_path
                                        fixed_count += 1
                                        print(f"  修复路径: {video_path} -> {new_path}")
                                        
                                        # 复制文件（如果目标文件不存在）
                                        target_path = os.path.join(os.path.dirname(json_file), "raw_video", new_filename)
                                        if not os.path.exists(target_path):
                                            import shutil
                                            shutil.copy2(original_path, target_path)
                                            print(f"  复制文件: {original_path} -> {target_path}")
        
        if fixed_count > 0:
            # 保存修改后的文件
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  修复了 {fixed_count} 个路径，已保存文件")
        else:
            print("  没有需要修复的路径")

if __name__ == "__main__":
    fix_incorrect_paths()
