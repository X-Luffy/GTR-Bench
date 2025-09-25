# GTR-Bench: 人类水平评估系统

一个基于Streamlit的视觉推理模型评估系统，支持人类答题和模型自动评估。

## 🎯 项目简介

GTR-Bench是一个综合性的视觉推理评估平台，旨在评估模型在复杂视觉场景下的推理能力。系统支持两种评估模式：

1. **人类答题评估**: 通过Web界面进行人工评估，建立人类基准
2. **模型自动评估**: 通过API调用自动评估各种视觉推理模型

## ✨ 主要特性

### 🧠 支持的任务类型
- **MotionState**: 运动状态推理
- **GeoLocation**: 地理位置推理  
- **ArrivalTimeInterval**: 到达时间间隔推理
- **CausalReordering**: 因果重排序推理
- **TrajectoryForecasting**: 轨迹预测
- **NextSpotForecasting**: 下一位置预测
- **MultiTargetTrajectoryForecasting**: 多目标轨迹预测

### 🌍 支持的数据场景
- **Indoor**: 室内场景
- **Outdoor**: 室外场景

### 🤖 模型评估功能
- 支持OpenAI兼容的API接口
- 实时进度监控
- 自动结果分析和可视化
- 支持批量评估和单案例测试

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Streamlit
- OpenCV
- PIL/Pillow
- NumPy
- Pandas

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动系统
```bash
# 方法1: 使用启动脚本
chmod +x run.sh
./run.sh

# 方法2: 直接启动
streamlit run app.py --server.port 8505
```

### 访问系统
打开浏览器访问: `http://localhost:8505`

## 📁 项目结构

```
├── app.py                          # 主应用文件
├── run.sh                          # 启动脚本
├── requirements.txt                 # 依赖包列表
├── README.md                       # 项目说明
├── README_EVAL_FEATURE.md          # 评估功能详细说明
├── .gitignore                      # Git忽略文件
├── data/                           # 数据目录
│   ├── indoor/                     # 室内场景数据
│   └── outdoor/                    # 室外场景数据
├── eval/                           # 评估模块
│   ├── eval.py                     # 主评估脚本
│   ├── eval_type.py                # 评估类型定义
│   ├── run_full_evaluation.sh      # 完整评估脚本
│   ├── results/                    # 评估结果目录
│   └── prompt/                     # 提示词模块
│       ├── question_info.py        # 问题信息
│       ├── map_info.py             # 地图信息
│       └── video_info.py           # 视频信息
├── utils/                          # 工具模块
│   ├── data_loader.py              # 数据加载器
│   ├── video_processor.py          # 视频处理器
│   └── scoring.py                  # 评分系统
└── components/                     # UI组件
    ├── question_display.py         # 问题显示组件
    └── result_display.py           # 结果显示组件
```

## 🎮 使用指南

### 人类答题评估
1. 在侧边栏选择场景和任务类型
2. 点击"🔄 加载题目数据"
3. 查看地图和摄像头图像
4. 回答问题并提交
5. 查看评分结果

### 模型自动评估
1. 点击"🚀 启动模型评估"
2. 配置模型参数（API Key、Base URL等）
3. 选择测试范围和案例数量
4. 点击"🚀 开始评估"
5. 实时监控评估进度
6. 查看评估结果

### 结果分析
1. 点击"📈 查看评估结果"
2. 选择评估结果文件
3. 查看统计信息和详细结果
4. 分析模型表现

## 🔧 配置说明

### 环境配置
- 确保Python环境已正确安装
- 安装所有必需的依赖包
- 配置conda环境（如需要）

### API配置
- 准备OpenAI兼容的API密钥
- 配置正确的Base URL
- 设置合适的模型参数

### 数据配置
- 确保数据文件位于正确的目录
- 检查数据文件格式是否正确
- 验证图像和视频文件路径

## 📊 评估指标

系统支持多种评估指标：

- **MCQ Accuracy**: 选择题准确率
- **Time IoU**: 时间范围重叠度
- **Overall Score**: 综合得分

详细指标说明请参考 `README_EVAL_FEATURE.md`。

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 [Issue](https://github.com/your-username/gtr-bench/issues)
- 发送邮件至: your-email@example.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和研究人员。

---

**注意**: 使用前请确保已正确配置所有必要的环境和数据文件。