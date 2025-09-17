# GTR-Bench 标准基准组织结构

本文档详细说明了 GTR-Bench 基准的标准文件组织结构和命名规范。

## 目录结构概览

```
GTR-Bench/
├── 📁 data/                     # 数据组织目录
│   ├── 📁 raw/                  # 原始未处理数据
│   ├── 📁 processed/            # 处理后的格式化数据
│   ├── 📁 annotations/          # 标注文件和元数据
│   ├── 📁 splits/              # 训练/验证/测试集划分
│   ├── 📁 samples/             # 示例数据集
│   └── 📁 tasks/               # 任务特定数据组织
│       ├── 📁 spatial_reasoning/      # 空间推理任务
│       ├── 📁 spatial_understanding/  # 空间理解任务
│       ├── 📁 spatial_navigation/     # 空间导航任务
│       └── 📁 object_relations/       # 对象关系任务
├── 📁 src/                     # 源代码目录
│   ├── 📁 gtr_bench/          # 主要基准包
│   │   ├── 📁 tasks/          # 任务实现
│   │   ├── 📁 metrics/        # 评估指标
│   │   └── 📁 datasets/       # 数据集加载器
│   ├── 📁 evaluation/         # 评估框架
│   ├── 📁 models/            # 模型封装和接口
│   ├── 📁 data_processing/   # 数据处理工具
│   └── 📁 utils/             # 通用工具
├── 📁 configs/               # 配置文件目录
│   ├── 📁 models/           # 模型配置
│   ├── 📁 tasks/            # 任务配置
│   ├── 📁 evaluation/       # 评估配置
│   └── 📁 datasets/         # 数据集配置
├── 📁 experiments/           # 实验管理
│   ├── 📁 runs/             # 单次实验运行
│   ├── 📁 logs/             # 实验日志
│   └── 📁 checkpoints/      # 模型检查点
├── 📁 results/              # 结果和分析
│   ├── 📁 outputs/          # 原始评估输出
│   ├── 📁 analysis/         # 分析脚本和笔记本
│   ├── 📁 reports/          # 生成的报告
│   └── 📁 leaderboard/      # 排行榜数据
├── 📁 scripts/              # 实用脚本
│   ├── 📁 data_processing/  # 数据预处理脚本
│   ├── 📁 evaluation/       # 评估运行脚本
│   ├── 📁 analysis/         # 分析和可视化脚本
│   └── 📁 setup/            # 设置和安装脚本
├── 📁 tests/                # 测试套件
│   ├── 📁 unit/             # 单元测试
│   ├── 📁 integration/      # 集成测试
│   └── 📁 fixtures/         # 测试数据和夹具
├── 📁 docs/                 # 文档
│   ├── 📁 api/              # API文档
│   ├── 📁 user_guide/       # 用户指南
│   ├── 📁 developer_guide/  # 开发者文档
│   └── 📁 assets/           # 文档资源
└── 📁 examples/             # 示例用法和教程
    ├── 📁 basic_evaluation/
    ├── 📁 custom_models/
    ├── 📁 data_preparation/
    └── 📁 analysis/
```

## 文件命名规范

### 数据文件
- **图像文件**: `{任务名}_{数据集}_{ID}.{扩展名}`
  - 示例: `spatial_reasoning_train_001.jpg`
- **标注文件**: `{任务名}_{数据集}_annotations.json`
  - 示例: `spatial_reasoning_train_annotations.json`
- **数据划分**: `{数据集}_ids.txt`
  - 示例: `train_ids.txt`, `val_ids.txt`, `test_ids.txt`

### 配置文件
- **模型配置**: `{模型名}.yaml`
  - 示例: `clip_large.yaml`, `blip2_opt.yaml`
- **任务配置**: `{任务名}.yaml`
  - 示例: `spatial_reasoning.yaml`

### 结果文件
- **评估输出**: `{模型}_{任务}_{时间戳}.json`
  - 示例: `clip_large_spatial_reasoning_20240101_120000.json`
- **报告文件**: `{实验名}_report_{日期}.pdf`
  - 示例: `baseline_experiment_report_20240101.pdf`

### 代码文件
- **任务实现**: `{任务名}_task.py`
  - 示例: `spatial_reasoning_task.py`
- **指标实现**: `{指标名}.py`
  - 示例: `spatial_accuracy.py`
- **模型封装**: `{模型名}_wrapper.py`
  - 示例: `clip_wrapper.py`

## 关键组件说明

### 📊 数据组织 (`data/`)
- **raw/**: 存储原始、未修改的数据集
- **processed/**: 清理、格式化后的数据
- **annotations/**: 真实标签和元数据
- **splits/**: 预定义的训练/验证/测试划分
- **tasks/**: 特定任务的数据组织

### 💻 源代码 (`src/`)
- **gtr_bench/**: 核心基准库
- **evaluation/**: 评估管道和运行器
- **models/**: 不同VLM架构的模型封装
- **data_processing/**: 数据加载和预处理工具

### ⚙️ 配置 (`configs/`)
包含以下类型的YAML配置文件：
- 模型设置和超参数
- 任务定义和参数
- 评估协议
- 数据集规范

### 🧪 实验 (`experiments/`)
- **runs/**: 单个实验输出
- **logs/**: 详细执行日志
- **checkpoints/**: 模型状态和中间结果

### 📈 结果 (`results/`)
- **outputs/**: 原始评估结果 (JSON, CSV)
- **analysis/**: 分析笔记本和可视化
- **reports/**: 格式化报告和摘要
- **leaderboard/**: 性能排名和比较

## 使用指南

### 1. 添加新任务
```bash
# 1. 创建任务配置
cp configs/tasks/spatial_reasoning.yaml configs/tasks/new_task.yaml

# 2. 实现任务类
touch src/gtr_bench/tasks/new_task.py

# 3. 添加数据目录
mkdir -p data/tasks/new_task

# 4. 更新任务注册表
# 编辑 src/gtr_bench/tasks/__init__.py
```

### 2. 添加新模型
```bash
# 1. 创建模型配置
touch configs/models/new_model.yaml

# 2. 实现模型封装
touch src/models/new_model_wrapper.py

# 3. 添加使用示例
touch examples/custom_models/new_model_example.py
```

### 3. 添加新指标
```bash
# 1. 实现指标函数
touch src/gtr_bench/metrics/new_metric.py

# 2. 注册指标
# 编辑 src/gtr_bench/metrics/__init__.py

# 3. 添加测试
touch tests/unit/test_new_metric.py
```

## 最佳实践

### 📋 版本控制
- 使用 Git LFS 管理大型数据文件
- 通过 `.gitignore` 排除生成的文件
- 维护清晰的提交历史

### 📚 文档
- 记录所有配置选项
- 提供使用示例
- 维护API文档

### 🧪 测试
- 为新组件添加单元测试
- 编写集成测试
- 保持高测试覆盖率

### 🔄 可重现性
- 固定依赖版本
- 使用随机种子
- 记录实验配置

### 🔧 模块化
- 保持组件松耦合
- 使用配置驱动的设计
- 遵循单一职责原则

## 快速开始

1. **克隆仓库**:
   ```bash
   git clone https://github.com/X-Luffy/GTR-Bench.git
   cd GTR-Bench
   ```

2. **安装依赖**:
   ```bash
   ./scripts/setup/install.sh
   ```

3. **运行示例**:
   ```bash
   python examples/basic_evaluation/simple_evaluation.py
   ```

4. **查看文档**:
   ```bash
   open docs/user_guide/benchmark_structure.md
   ```

这个标准化的结构确保了基准的可扩展性、可维护性和易用性，便于研究者添加新的数据、模型和评估方法。