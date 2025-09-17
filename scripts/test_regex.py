#!/usr/bin/env python3
import re

# 测试路径
test_paths = [
    "/home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/train/S04/c021/vdo.avi",
    "/home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/train/S04/c020/vdo.avi",
    "/home/mnt/xieqinghongbing/data/cityflow/AICity22_Track1_MTMC_Tracking/track_processed/S04/259/video/52_59_c020.mp4"
]

print("测试cityflow路径匹配:")
for path in test_paths:
    print(f"\n路径: {path}")
    
    # 测试video_path匹配
    if "train/" in path:
        match = re.search(r'/train/([^/]+)/([^/]+)/', path)
        if match:
            scene, camera = match.groups()
            ext = path.split('.')[-1] if '.' in path else ''
            new_name = f"cityflow_{scene}_{camera}.{ext}"
            print(f"  video_path匹配成功: {new_name}")
        else:
            print(f"  video_path匹配失败")
    
    # 测试crop_video_path匹配
    if "track_processed/" in path:
        match = re.search(r'/track_processed/([^/]+)/([^/]+)/video/([^/]+)', path)
        if match:
            scene, obj_id, filename = match.groups()
            new_name = f"cityflow_{scene}_{obj_id}_{filename}"
            print(f"  crop_video_path匹配成功: {new_name}")
        else:
            print(f"  crop_video_path匹配失败")
