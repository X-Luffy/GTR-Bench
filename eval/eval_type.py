"""
GTR-Bench 评估类型定义
定义七种任务类型及其对应的评估指标
"""

# 任务类型与评估指标的映射
EVAL_TYPES = {
    "GeoLocation": "MCQ_Acc",           # 地理位置推理 - 选择题准确率
    "ArrivalTimeInterval": "MCQ_Acc",  # 到达时间间隔推理 - 选择题准确率
    "MotionState": "MCQ_Acc",           # 运动状态推理 - 选择题准确率
    "CausalReordering": "MCQ_Acc",      # 因果重排序推理 - 选择题准确率
    "NextSpotForecasting": "ST-IoU",   # 下一位置预测 - 选择题+时间范围IoU
    "TrajectoryForecasting": "ST-IoU",  # 轨迹预测 - 选择题+时间范围IoU
    "MultiTargetTrajectoryForecasting": "ST-IoU"  # 多轨迹预测 - 选择题+时间范围IoU
}

# 评估类型说明
EVAL_TYPE_DESCRIPTIONS = {
    "MCQ_Acc": {
        "name": "Multiple Choice Question Accuracy",
        "description": "选择题准确率评估",
        "metrics": ["accuracy_score"],
        "calculation": "选择题是否正确"
    },
    "ST-IoU": {
        "name": "Spatial-Temporal Intersection over Union",
        "description": "空间-时间交并比评估",
        "metrics": ["accuracy_score", "time_score"],
        "calculation": "选择题是否正确 + 时间范围IoU"
    }
}

def get_eval_type(task_name):
    """
    获取任务对应的评估类型
    
    Args:
        task_name (str): 任务名称
        
    Returns:
        str: 评估类型 (MCQ_Acc 或 ST-IoU)
    """
    return EVAL_TYPES.get(task_name, "MCQ_Acc")

def get_eval_description(eval_type):
    """
    获取评估类型的详细描述
    
    Args:
        eval_type (str): 评估类型
        
    Returns:
        dict: 评估类型描述
    """
    return EVAL_TYPE_DESCRIPTIONS.get(eval_type, {})

def is_mcq_task(task_name):
    """
    判断是否为选择题任务
    
    Args:
        task_name (str): 任务名称
        
    Returns:
        bool: 是否为选择题任务
    """
    return get_eval_type(task_name) == "MCQ_Acc"

def is_st_iou_task(task_name):
    """
    判断是否为ST-IoU任务
    
    Args:
        task_name (str): 任务名称
        
    Returns:
        bool: 是否为ST-IoU任务
    """
    return get_eval_type(task_name) == "ST-IoU"

# 任务类型列表
TASK_TYPES = list(EVAL_TYPES.keys())

# MCQ任务列表
MCQ_TASKS = [task for task, eval_type in EVAL_TYPES.items() if eval_type == "MCQ_Acc"]

# ST-IoU任务列表
ST_IOU_TASKS = [task for task, eval_type in EVAL_TYPES.items() if eval_type == "ST-IoU"]
