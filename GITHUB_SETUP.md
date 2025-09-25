# GitHub 上传指南

## 🚀 项目已准备就绪

项目已经完成所有准备工作，可以上传到GitHub了！

## ✅ 已完成的准备工作

### 1. 路径清理
- ✅ 清理了所有硬编码的本地路径
- ✅ 使用相对路径和动态路径解析
- ✅ 确保代码在不同环境下都能正常运行

### 2. 项目文档
- ✅ 创建了完整的 `README.md`
- ✅ 创建了 `README_EVAL_FEATURE.md` 详细说明
- ✅ 创建了 `requirements.txt` 依赖列表
- ✅ 创建了 `LICENSE` 许可证文件

### 3. Git配置
- ✅ 创建了 `.gitignore` 文件
- ✅ 初始化了Git仓库
- ✅ 提交了所有更改

## 📋 上传到GitHub的步骤

### 1. 在GitHub上创建新仓库
1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮
3. 选择 "New repository"
4. 填写仓库信息：
   - **Repository name**: `gtr-bench` 或 `human-level-evaluation`
   - **Description**: `GTR-Bench: Human-level Visual Reasoning Evaluation System`
   - **Visibility**: Public 或 Private（根据您的需要）
   - **不要**勾选 "Initialize this repository with a README"

### 2. 连接本地仓库到GitHub
```bash
# 添加远程仓库（替换为您的GitHub用户名和仓库名）
git remote add origin https://github.com/YOUR_USERNAME/gtr-bench.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 3. 验证上传
1. 访问您的GitHub仓库页面
2. 确认所有文件都已正确上传
3. 检查README.md是否正确显示

## 🔧 后续配置建议

### 1. 设置仓库描述
在GitHub仓库页面添加：
- **Description**: `A comprehensive visual reasoning evaluation system supporting human assessment and automated model evaluation`
- **Topics**: `visual-reasoning`, `evaluation`, `streamlit`, `computer-vision`, `benchmark`

### 2. 创建Release
1. 在GitHub仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `GTR-Bench v1.0.0 - Initial Release`
   - **Description**: 复制README.md中的项目介绍

### 3. 设置GitHub Pages（可选）
如果需要展示项目：
1. 进入仓库的 "Settings"
2. 找到 "Pages" 部分
3. 选择 "Deploy from a branch"
4. 选择 "main" 分支和 "/ (root)" 文件夹

## 📝 使用说明

### 对于新用户
1. 克隆仓库：
   ```bash
   git clone https://github.com/YOUR_USERNAME/gtr-bench.git
   cd gtr-bench
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 启动系统：
   ```bash
   streamlit run app.py --server.port 8505
   ```

### 对于贡献者
1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request

## 🎯 项目特色

- **完整的评估系统**: 支持人类答题和模型自动评估
- **7种任务类型**: 覆盖多种视觉推理场景
- **实时监控**: 评估进度实时显示
- **结果可视化**: 详细的统计分析和结果展示
- **易于扩展**: 模块化设计，便于添加新功能

## 📞 支持

如有问题，请：
1. 查看 `README.md` 和 `README_EVAL_FEATURE.md`
2. 创建 [Issue](https://github.com/YOUR_USERNAME/gtr-bench/issues)
3. 联系项目维护者

---

**恭喜！您的项目已准备好上传到GitHub！** 🎉
