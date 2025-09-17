import json
from collections import defaultdict

def verify_duplicates(json_file_path):
    """验证并显示案例信息"""
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 总案例数: {len(data['cases'])}")
    print("=" * 80)
    
    # 存储每个crop_video_path组合对应的案例
    video_path_to_cases = defaultdict(list)
    
    # 遍历所有案例并显示前几个案例的信息
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
        
        # 显示前5个案例的详细信息
        if i < 5:
            print(f"\n📋 案例 {i+1}:")
            print(f"  案例ID: {case_info['case_id']}")
            print(f"  场景: {case_info['scene']}")
            print(f"  目标ID: {case_info['object_id']}")
            print(f"  视频路径数量: {len(crop_video_paths)}")
            for j, path in enumerate(crop_video_paths, 1):
                print(f"    {j}. {path}")
    
    # 找出重复的案例
    duplicates = {}
    for video_path_key, cases in video_path_to_cases.items():
        if len(cases) > 1:
            duplicates[video_path_key] = cases
    
    print("\n" + "=" * 80)
    print("🔍 重复检查结果:")
    
    if not duplicates:
        print("✅ 没有发现重复的案例")
        print(f"📈 统计信息:")
        print(f"  总案例数: {len(data['cases'])}")
        print(f"  唯一视频路径组合数: {len(video_path_to_cases)}")
        print(f"  每个案例都有独特的视频路径组合")
    else:
        print(f"❌ 发现 {len(duplicates)} 组重复案例:")
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
    verify_duplicates(json_file_path)

