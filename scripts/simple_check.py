import json
from collections import defaultdict

def check_duplicates(json_file_path):
    """检查JSON文件中的重复案例"""
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 总案例数: {len(data['cases'])}")
    
    # 存储每个crop_video_path组合对应的案例
    video_path_to_cases = defaultdict(list)
    
    # 遍历所有案例
    for i, case in enumerate(data['cases']):
        # 提取crop_video_path列表
        crop_video_paths = []
        for camera in case['camera_images']:
            if 'crop_video_path' in camera:
                crop_video_paths.append(camera['crop_video_path'])
        
        # 排序以确保相同路径组合的一致性
        crop_video_paths.sort()
        video_path_key = tuple(crop_video_paths)
        
        # 记录案例信息
        case_info = {
            'index': i,
            'case_id': case.get('case_id', f'Case_{i}'),
            'scene': case.get('scene', 'Unknown'),
            'object_id': case.get('camera_images', [{}])[0].get('object_id', 'Unknown') if case.get('camera_images') else 'Unknown'
        }
        
        video_path_to_cases[video_path_key].append(case_info)
    
    # 找出重复的案例
    duplicates = {}
    for video_path_key, cases in video_path_to_cases.items():
        if len(cases) > 1:
            duplicates[video_path_key] = cases
    
    print(f"🔍 重复检查结果:")
    
    if not duplicates:
        print("✅ 没有发现重复的案例")
        return
    
    print(f"❌ 发现 {len(duplicates)} 组重复案例:")
    print("=" * 80)
    
    for i, (video_path_key, cases) in enumerate(duplicates.items(), 1):
        print(f"\n📋 重复组 {i} (共 {len(cases)} 个案例):")
        print("🎬 共享的视频路径:")
        for j, path in enumerate(video_path_key, 1):
            print(f"  {j}. {path}")
        print("📝 重复案例:")
        for case in cases:
            print(f"  • 索引: {case['index']}, 案例ID: {case['case_id']}, 场景: {case['scene']}, 目标ID: {case['object_id']}")

if __name__ == "__main__":
    json_file_path = "data/cityflow/cityflow_MotionReasoning_30.json"
    check_duplicates(json_file_path)

