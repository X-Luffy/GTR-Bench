#!/bin/bash

# 人类水平评估系统启动脚本

echo "🎯 启动人类水平评估系统..."

# 激活conda环境
echo "🔧 激活conda环境..."
conda activate /home/mnt/xieqinghongbing/env/open_manus

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装，请先安装Python"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
python -c "import streamlit, cv2, PIL, numpy, pandas; print('✅ 所有依赖都已安装')" || {
    echo "❌ 缺少依赖，请安装requirements.txt中的包"
    exit 1
}

# 启动应用
echo "🚀 启动Streamlit应用..."
streamlit run app.py --server.port 8505 --server.address 0.0.0.0
