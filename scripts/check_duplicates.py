import json
from collections import defaultdict

def check_duplicate_cases(json_file_path):
    """检查JSON文件中的重复案例"""
    
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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
        
        # 将路径组合转换为元组作为键
        video_path_key = tuple(crop_video_paths)
        
        # 记录案例信息
        case_info = {
            'index': i,
            'case_id': case.get('case_id', f'Case_{i}'),
            'scene': case.get('scene', 'Unknown'),
            'object_id': case.get('camera_images', [{}])[0].get('object_id', 'Unknown') if case.get('camera_images') else 'Unknown',
            'crop_video_paths': crop_video_paths
        }
        
        video_path_to_cases[video_path_key].append(case_info)
    
    # 找出重复的案例
    duplicates = {}
    for video_path_key, cases in video_path_to_cases.items():
        if len(cases) > 1:
            duplicates[video_path_key] = cases
    
    return duplicates

def print_duplicates(duplicates):
    """打印重复案例的详细信息"""
    if not duplicates:
        print("✅ 没有发现重复的案例")
        return
    
    print(f"🔍 发现 {len(duplicates)} 组重复案例:")
    print("=" * 80)
    
    for i, (video_path_key, cases) in enumerate(duplicates.items(), 1):
        print(f"\n📋 重复组 {i} (共 {len(cases)} 个案例):")
        print("-" * 60)
        
        # 打印视频路径
        print("🎬 共享的视频路径:")
        for j, path in enumerate(video_path_key, 1):
            print(f"  {j}. {path}")
        
        # 打印每个重复案例的详细信息
        print("\n📝 重复案例详情:")
        for case in cases:
            print(f"  • 索引: {case['index']}")
            print(f"    案例ID: {case['case_id']}")
            print(f"    场景: {case['scene']}")
            print(f"    目标ID: {case['object_id']}")
            print()

if __name__ == "__main__":
    json_file_path = "data/cityflow/cityflow_MotionReasoning_30.json"
    
    try:
        duplicates = check_duplicate_cases(json_file_path)
        print_duplicates(duplicates)
    except FileNotFoundError:
        print(f"❌ 文件未找到: {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

