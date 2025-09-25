#!/bin/bash

# 人类水平评估系统启动脚本

echo "🎯 启动人类水平评估系统..."

# 激活conda环境
echo "🔧 激活conda环境..."
# 注意：请根据您的实际conda环境路径修改以下路径
# conda activate your_conda_environment_name
echo "⚠️  请手动激活您的conda环境，例如：conda activate your_env_name"

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装，请先安装Python"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
python -c "import streamlit, cv2, PIL, numpy, pandas, subprocess, threading, queue; print('✅ 所有依赖都已安装')" || {
    echo "❌ 缺少依赖，请安装requirements.txt中的包"
    exit 1
}

# 检查eval目录
if [ ! -d "eval" ]; then
    echo "❌ eval目录不存在，请确保eval目录存在"
    exit 1
fi

# 检查eval.py
if [ ! -f "eval/eval.py" ]; then
    echo "❌ eval/eval.py文件不存在"
    exit 1
fi

# 创建必要目录
echo "📁 创建必要目录..."
mkdir -p eval/results
mkdir -p eval/results/prompt

# 启动应用
echo "🚀 启动Streamlit应用..."
echo "📊 系统功能："
echo "   - 人类答题评估"
echo "   - 模型自动评估"
echo "   - 结果可视化分析"
echo "   - 实时进度监控"
echo ""
echo "🌐 访问地址: http://localhost:8505"
echo "⏹️  按 Ctrl+C 停止服务"
echo ""

streamlit run app.py --server.port 8506 --server.address 0.0.0.0
