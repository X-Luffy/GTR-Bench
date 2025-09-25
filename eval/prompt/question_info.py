"""
GTR-Bench 问题提示模板
定义不同任务类型的问题提示规则
"""

MCQ_ANSWER_RULE_EN = """
Question:
{question}
Options:
{choices}

Please answer according to the following rules:
0. You need to select one option as the answer.
1. **Provide brief explanation**: After selection, briefly explain your reasoning, especially why certain options are excluded.
2. **Pay attention to time and spatial information**: If the question involves time or space, ensure your choice is consistent with this information.
3. **Follow question requirements**: If the question has specific format or requirements, strictly comply with them.

Please return the answer in the following JSON format:
{{
    "answer": "correct answer",
    "explanation": "brief explanation of your choice reasoning",
    "reasoning": "detailed reasoning process and analysis"
}}
"""

MCQ_TIME_IOU_RULE_EN = """
Question:
{question}
Options:
{choices}

Please answer according to the following rules:
0. You need to select one option as the answer and infer a time range.
1. **Provide brief explanation**: After selection, briefly explain your reasoning, especially why certain options are excluded.
2. **Pay attention to time and spatial information**: If the question involves time or space, ensure your choice is consistent with this information.
3. **Follow question requirements**: If the question has specific format or requirements, strictly comply with them.
4. **Time range analysis**: Please carefully analyze the given time range and ensure your answer is consistent with the time range.
5. **Time format**: Please use HH:MM:SS.mmm to represent time.

Please return the answer in the following JSON format:
{{
    "answer": "correct answer",
    "time_duration": ["start_time_str-end_time_str"],  # time range
    "explanation": "brief explanation of your choice reasoning",
    "reasoning": "detailed reasoning process and analysis"
}}
"""

MCQ_TIME_IOU_TS_RULE_EN = """
Question:
{question}
Options:
{choices}

Please answer according to the following rules:
0. You need to select a correct option sequence and infer a time range sequence simultaneously.
1. **Provide brief explanation**: After selection, briefly explain your reasoning, especially why certain options are excluded.
2. **Pay attention to time and spatial information**: If the question involves time or space, ensure your choice is consistent with this information.
3. **Follow question requirements**: If the question has specific format or requirements, strictly comply with them.
4. **Time range analysis**: Please carefully analyze the given time range and ensure your answer is consistent with the time range.
5. **Time format**: Please use HH:MM:SS.mmm to represent time.

Please return the answer in the following JSON format:
{{
    "answer": ["correct answer1", "correct answer2"...],  
    "time_duration": ["start_time_str-end_time_str","start_time_str-end_time_str"],  # time range
    "explanation": "brief explanation of your choice reasoning",
    "reasoning": "detailed reasoning process and analysis"
}}
"""

TF_MCQ_TIME_IOU_RULE_EN = """
Question:
{question}
Options:
{choices}

Please answer according to the following rules:
0. You first need to determine whether it is true or false (TF), then select a correct option, and predict a time range.
1. **Provide brief explanation**: After selection, briefly explain your reasoning, especially why certain options are excluded.
2. **Pay attention to time and spatial information**: If the question involves time or space, ensure your choice is consistent with this information.
3. **Follow question requirements**: If the question has specific format or requirements, strictly comply with them.
4. **Time range analysis**: Please carefully analyze the given time range and ensure your answer is consistent with the time range.
5. **Time format**: Please use HH:MM:SS.mmm to represent time.

Please return the answer in the following JSON format:
{{
    "TF": true/false,  
    "answer": "correct answer",
    "time_duration": ["start_time_str-end_time_str"],  # time range
    "explanation": "brief explanation of your choice reasoning",
    "reasoning": "detailed reasoning process and analysis"
}}
"""

# 任务类型与提示规则的映射
ANSWER_RULE_EN = {
    "GeoLocation": MCQ_ANSWER_RULE_EN,
    "ArrivalTimeInterval": MCQ_ANSWER_RULE_EN,
    "MotionState": MCQ_ANSWER_RULE_EN,
    "CausalReordering": MCQ_ANSWER_RULE_EN,
    "NextSpotForecasting": MCQ_TIME_IOU_RULE_EN,
    "TrajectoryForecasting": MCQ_TIME_IOU_TS_RULE_EN,
    "MultiTargetTrajectoryForecasting": TF_MCQ_TIME_IOU_RULE_EN,
}

def make_question_prompt(case):
    """
    根据案例创建问题提示
    
    Args:
        case (dict): 案例数据
        
    Returns:
        list: 消息列表
    """
    messages = []
    question = case['question']
    choices = '\n'.join(case['choices'])
    task_id = case.get('task_id', '')
    
    # 获取对应的提示规则
    rule_template = ANSWER_RULE_EN.get(task_id, MCQ_ANSWER_RULE_EN)
    
    messages.append({
        'type': 'text', 
        'text': rule_template.format(question=question, choices=choices)
    })

    return messages