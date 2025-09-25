"""
GTR-Bench 评估类型定义
Define seven task types and their corresponding evaluation metrics
"""

# Mapping of task types to evaluation metrics
EVAL_TYPES = {
    "GeoLocation": "MCQ_Acc",           # Geographic location reasoning - MCQ accuracy
    "ArrivalTimeInterval": "MCQ_Acc",  # Arrival time interval reasoning - MCQ accuracy
    "MotionState": "MCQ_Acc",           # Motion state reasoning - MCQ accuracy
    "CausalReordering": "MCQ_Acc",      # Causal reordering reasoning - MCQ accuracy
    "NextSpotForecasting": "ST-IoU",   # Next spot forecasting - MCQ + time range IoU
    "TrajectoryForecasting": "ST-IoU",  # Trajectory forecasting - MCQ + time range IoU
    "MultiTargetTrajectoryForecasting": "ST-IoU"  # Multi-target trajectory forecasting - MCQ + time range IoU
}

# Evaluation type descriptions
EVAL_TYPE_DESCRIPTIONS = {
    "MCQ_Acc": {
        "name": "Multiple Choice Question Accuracy",
        "description": "Multiple choice question accuracy evaluation",
        "metrics": ["accuracy_score"],
        "calculation": "Whether multiple choice question is correct"
    },
    "ST-IoU": {
        "name": "Spatial-Temporal Intersection over Union",
        "description": "Spatial-temporal intersection over union evaluation",
        "metrics": ["accuracy_score", "time_score"],
        "calculation": "Whether MCQ is correct + time range IoU"
    }
}

def get_eval_type(task_name):
    """
    Get evaluation type corresponding to task
    
    Args:
        task_name (str): Task name
        
    Returns:
        str: Evaluation type (MCQ_Acc or ST-IoU)
    """
    return EVAL_TYPES.get(task_name, "MCQ_Acc")

def get_eval_description(eval_type):
    """
    Get detailed description of evaluation type
    
    Args:
        eval_type (str): Evaluation type
        
    Returns:
        dict: Evaluation type description
    """
    return EVAL_TYPE_DESCRIPTIONS.get(eval_type, {})

def is_mcq_task(task_name):
    """
    Determine if it is an MCQ task
    
    Args:
        task_name (str): Task name
        
    Returns:
        bool: Whether it is an MCQ task
    """
    return get_eval_type(task_name) == "MCQ_Acc"

def is_st_iou_task(task_name):
    """
    Determine if it is an ST-IoU task
    
    Args:
        task_name (str): Task name
        
    Returns:
        bool: Whether it is an ST-IoU task
    """
    return get_eval_type(task_name) == "ST-IoU"

# Task type list
TASK_TYPES = list(EVAL_TYPES.keys())

# MCQ task list
MCQ_TASKS = [task for task, eval_type in EVAL_TYPES.items() if eval_type == "MCQ_Acc"]

# ST-IoU task list
ST_IOU_TASKS = [task for task, eval_type in EVAL_TYPES.items() if eval_type == "ST-IoU"]
