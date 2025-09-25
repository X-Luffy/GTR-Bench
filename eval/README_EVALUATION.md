# GTR-Bench Evaluation System

## Overview

This evaluation system is used to test the performance of visual reasoning models on the GTR-Bench dataset. The system supports multiple task types including trajectory prediction, time interval prediction, etc.

## Main Features

### 1. Consolidated Result Files
- Results from all test cases will be saved in a single JSON file
- Filename format: `{model_name}_{timestamp}.json`
- 例如：`claude_sonnet_4_20250514_thinking_20250925_143000.json`

### 2. Prompt文件管理
- 每个案例的完整对话记录保存在单独的prompt文件中
- Filename format: `prompt_{model_name}_{case_id}_{task_id}_{timestamp}.json`
- 所有prompt文件保存在`results/prompt/`目录下

### 3. 结果文件结构
```json
[
  {
    "case_id": "案例ID",
    "scene": "场景类型（indoor/outdoor）",
    "task_id": "任务类型",
    "question": "问题内容",
    "response": {
      "model_answer": "模型原始回答",
      "answer": ["提取的答案选项"],
      "time_duration": ["时间范围"],
      "ground_truth": {
        "correct_cam_name": ["正确答案"],
        "correct_time_str": ["正确时间范围"]
      }
    },
    "metrics": {
      "score": 0.xxx,
      "MCQacc": 0.xxx,
      "TimeIoU": 0.xxx
    },
    "timestamp": "时间戳"
  }
]
```

## Usage

### 1. 完整评估（420个案例）
```bash
./run_full_evaluation.sh
```

### 2. 测试评估（2个案例）
```bash
./test_evaluation.sh
```

### 3. 自定义评估
```bash
python eval.py \
    --model "模型名称" \
    --api-key "API密钥" \
    --base-url "API地址" \
    --data-dir "../data" \
    --result-dir "./results" \
    --max-cases 10 \
    --verbose
```

## 参数说明

- `--model`: 模型名称（如：claude-sonnet-4-20250514-thinking）
- `--api-key`: OpenAI API密钥
- `--base-url`: API基础URL（可选）
- `--data-dir`: 数据目录路径
- `--result-dir`: 结果保存目录
- `--max-cases`: 最大测试案例数（用于测试）
- `--case-id`: 指定特定案例ID
- `--scene`: 按场景过滤（indoor/outdoor）
- `--task-type`: 按任务类型过滤
- `--verbose`: 启用详细输出

## 输出文件

### 结果文件
- 位置：`results/{model_name}_{timestamp}.json`
- 内容：包含所有测试案例的完整结果

### Prompt文件
- 位置：`results/prompt/prompt_{model_name}_{case_id}_{task_id}_{timestamp}.json`
- 内容：包含完整的对话记录和评估信息

## 评估指标

- **Score**: 综合得分
- **MCQacc**: 多选题准确率
- **TimeIoU**: 时间范围IoU得分

## Notes

1. 确保数据目录结构正确
2. API密钥需要有足够的额度
3. 评估过程可能需要较长时间，建议使用screen或tmux
4. 结果文件会自动覆盖同名文件，请注意备份

## 故障排除

1. **API错误**: 检查API密钥和网络连接
2. **路径错误**: 确认数据目录和文件路径正确
3. **内存不足**: 减少并发数量或分批处理
4. **文件权限**: 确保脚本有执行权限
