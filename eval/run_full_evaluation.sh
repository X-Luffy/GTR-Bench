#!/bin/bash

# GTR-Bench 完整评估脚本
# 测试所有420道题目（indoor/outdoor各7种任务类型，每种30道题）

# 配置参数
API_KEY="sk-XXXXXXXXXXXx"
BASE_URL="xxxxxxxx"
MODEL_NAME="XXXXXXX"

# 数据目录
DATA_DIR="../data"

# 结果目录
RESULT_DIR="./results"
PROMPT_DIR="./results/prompt"

# 创建结果目录
mkdir -p "$RESULT_DIR"
mkdir -p "$PROMPT_DIR"

echo "=========================================="
echo "GTR-Bench 完整评估开始"
echo "=========================================="
echo "模型: $MODEL_NAME"
echo "API Key: ${API_KEY:0:20}..."
echo "Base URL: $BASE_URL"
echo "数据目录: $DATA_DIR"
echo "结果目录: $RESULT_DIR"
echo "=========================================="

# 检查数据目录是否存在
if [ ! -d "$DATA_DIR" ]; then
    echo "错误: 数据目录不存在: $DATA_DIR"
    exit 1
fi

# 检查eval.py是否存在
if [ ! -f "eval.py" ]; then
    echo "错误: eval.py文件不存在"
    exit 1
fi

# 开始评估
echo "开始评估所有420道题目..."
echo "时间: $(date)"

# 调用eval.py进行完整评估
python eval.py \
    --model "$MODEL_NAME" \
    --api-key "$API_KEY" \
    --base-url "$BASE_URL" \
    --data-dir "$DATA_DIR" \
    --result-dir "$RESULT_DIR" \
    --verbose

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "=========================================="
    echo "评估完成！"
    echo "时间: $(date)"
    echo "=========================================="
    
    # 显示结果统计
    echo "结果文件统计:"
    echo "- 结果JSON文件数量: $(find $RESULT_DIR -name "*.json" -not -path "*/prompt/*" | wc -l)"
    echo "- Prompt文件数量: $(find $PROMPT_DIR -name "*.json" | wc -l)"
    
    # 显示最新的结果文件
    LATEST_RESULT=$(find $RESULT_DIR -name "*.json" -not -path "*/prompt/*" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
    if [ -n "$LATEST_RESULT" ]; then
        echo "- 最新结果文件: $(basename $LATEST_RESULT)"
        
        # 显示结果文件中的案例数量
        CASE_COUNT=$(python -c "
import json
try:
    with open('$LATEST_RESULT', 'r') as f:
        data = json.load(f)
    print(len(data))
except:
    print('0')
")
        echo "- 评估案例数量: $CASE_COUNT"
        
        # 显示按场景和任务类型的统计
        echo "- 按场景统计:"
        python -c "
import json
try:
    with open('$LATEST_RESULT', 'r') as f:
        data = json.load(f)
    
    scenes = {}
    tasks = {}
    
    for case in data:
        scene = case.get('scene', 'unknown')
        task = case.get('task_id', 'unknown')
        
        scenes[scene] = scenes.get(scene, 0) + 1
        tasks[task] = tasks.get(task, 0) + 1
    
    print('  场景分布:')
    for scene, count in scenes.items():
        print(f'    {scene}: {count} cases')
    
    print('  任务类型分布:')
    for task, count in tasks.items():
        print(f'    {task}: {count} cases')
        
except Exception as e:
    print(f'  统计失败: {e}')
"
    fi
    
    echo "=========================================="
    echo "评估结果已保存到: $RESULT_DIR"
    echo "Prompt文件已保存到: $PROMPT_DIR"
    echo "=========================================="
else
    echo "=========================================="
    echo "评估失败！"
    echo "时间: $(date)"
    echo "=========================================="
    exit 1
fi

