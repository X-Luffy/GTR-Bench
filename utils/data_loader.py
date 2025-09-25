import json
import os
from typing import Dict, List, Optional

class DataLoader:
    """Data loader class responsible for loading and managing question data"""
    
    def __init__(self):
        self.data = None
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        
    def load_data(self, scene: str, task_type: str) -> Dict:
        """
        加载指定场景和任务类型的数据
        
        Args:
            scene: 场景名称 (cityflow 或 mtmmc)
            task_type: Task type
            
        Returns:
            加载的数据字典
        """
        # Build file path
        filename = f"{scene}_{task_type}_30.json"
        file_path = os.path.join(self.base_path, scene, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"数据文件不存在: {file_path}")
        
        # 加载JSON数据
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        return self.data
    
    def get_case(self, case_index: int) -> Optional[Dict]:
        """
        获取指定索引的题目案例
        
        Args:
            case_index: 案例索引
            
        Returns:
            案例数据字典，如果索引无效则返回None
        """
        if not self.data or 'cases' not in self.data:
            return None
        
        cases = self.data['cases']
        if 0 <= case_index < len(cases):
            return cases[case_index]
        
        return None
    
    def get_total_cases(self) -> int:
        """
        获取总题目数量
        
        Returns:
            总题目数量
        """
        if not self.data or 'cases' not in self.data:
            return 0
        
        return len(self.data['cases'])
    
    def get_task_info(self) -> Dict:
        """
        获取任务信息
        
        Returns:
            任务信息字典
        """
        if not self.data:
            return {}
        
        return {
            'dataset_name': self.data.get('dataset_name', ''),
            'version': self.data.get('version', ''),
            'description': self.data.get('description', ''),
            'total_cases': self.get_total_cases()
        }
    
    def validate_case(self, case: Dict) -> bool:
        """
        验证案例数据的完整性
        
        Args:
            case: 案例数据字典
            
        Returns:
            验证是否通过
        """
        required_fields = ['case_id', 'question', 'ground_truth']
        
        for field in required_fields:
            if field not in case:
                return False
        
        return True
    
    def get_available_scenes(self) -> List[str]:
        """
        获取可用的场景列表
        
        Returns:
            场景列表
        """
        scenes = []
        if os.path.exists(self.base_path):
            for item in os.listdir(self.base_path):
                item_path = os.path.join(self.base_path, item)
                if os.path.isdir(item_path):
                    scenes.append(item)
        
        return scenes
    
    def get_available_tasks(self, scene: str) -> List[str]:
        """
        获取指定场景下可用的任务类型列表
        
        Args:
            scene: 场景名称
            
        Returns:
            任务类型列表
        """
        tasks = []
        scene_path = os.path.join(self.base_path, scene)
        
        if os.path.exists(scene_path):
            for item in os.listdir(scene_path):
                if item.endswith('_30.json'):
                    # 提取任务类型名称
                    task_name = item.replace(f'{scene}_', '').replace('_30.json', '')
                    tasks.append(task_name)
        
        return tasks
