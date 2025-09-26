# GTR-Bench: Evaluating Geo-Temporal Reasoning in Vision-Language Models

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 Abstract

Recent advances in spatial-temporal intelligence of Vision-Language Models (VLMs) have gained significant attention due to their critical importance for Autonomous Driving, Embodied AI, and General Artificial Intelligence. However, existing spatial-temporal benchmarks primarily focus on either:

- **Egocentric perspective reasoning** with images/video context, or
- **Geographic perspective reasoning** with graphics context (e.g., maps)

This limitation fails to assess VLMs' geographic spatial-temporal intelligence that combines both images/video and graphics context—a capability essential for applications like traffic management and emergency response.

### 🎯 Our Contribution

We introduce **GTR-Bench** (Geo-Temporal Reasoning Benchmark), a novel challenge for geographic temporal reasoning of moving targets in large-scale camera networks. GTR-Bench presents unique challenges:

- **Multi-perspective reasoning**: Switching between maps and videos
- **Cross-camera inference**: Joint reasoning across multiple videos with non-overlapping fields of view
- **Spatial-temporal prediction**: Inference over unobserved regions

### 📊 Key Findings

Evaluation of 10+ popular VLMs on GTR-Bench reveals significant performance gaps:

- **Best proprietary model** (Gemini-2.5-Pro): 34.9%
- **Human performance**: 78.61%
- **Performance gap**: 43.71%

### 🔍 Model Deficiencies Identified

1. **Imbalanced context utilization**: VLMs struggle with balanced spatial-temporal reasoning
2. **Temporal forecasting weakness**: Poor performance on temporal-emphasized tasks
3. **Map-video alignment**: Limited proficiency in comprehending map data with multi-view video inputs

**Repository**: https://anonymous.4open.science/r/GTR-Bench-5B76

## ✨ Key Features

### 🧠 Supported Task Types
| Task Type | Description | Difficulty |
|-----------|-------------|------------|
| **MotionState** | Infer target's motion state from video information | ⭐⭐ |
| **GeoLocation** | Determine spatial position relationships | ⭐⭐ |
| **ArrivalTimeInterval** | Predict temporal sequence of events | ⭐⭐⭐ |
| **CausalReordering** | Infer causal relationships between events | ⭐⭐⭐ |
| **TrajectoryForecasting** | Predict next two camera locations + time ranges | ⭐⭐⭐⭐ |
| **NextSpotForecasting** | Predict next location + time range | ⭐⭐⭐ |
| **MultiTargetTrajectoryForecasting** | Predict multiple targets' trajectories | ⭐⭐⭐⭐⭐ |

### 🌍 Supported Data Scenarios
- **🏠 Indoor**: Multi-modal camera tracking scenarios
- **🌆 Outdoor**: Vehicle tracking and re-identification scenarios

### 🤖 Model Evaluation Features
- ✅ **OpenAI-compatible API** interface support
- 📊 **Real-time progress** monitoring
- 📈 **Automatic result analysis** and visualization
- 🔄 **Batch evaluation** and single case testing
- 🎯 **Human baseline** comparison

## 🚀 Quick Start

### 📋 Prerequisites
- **Python**: 3.8+ (recommended: 3.9+)
- **Conda**: For environment management (optional)
- **Memory**: 8GB+ RAM recommended
- **Storage**: 10GB+ free space for datasets

### 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/X-Luffy/GTR-Bench.git
cd GTR-Bench
```

2. **Create conda environment (recommended)**
```bash
conda create -n gtr-bench python=3.9
conda activate gtr-bench
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 📊 Data Preparation

> ⚠️ **Important**: Before using GTR-Bench, you need to download and prepare the required datasets.

#### 🌆 Outdoor Scenarios (CityFlow Dataset)
```bash
# Download from AI City Challenge
# Source: https://www.aicitychallenge.org/
# Purpose: Vehicle tracking and re-identification

# Expected directory structure:
./data/outdoor/cityflow/
└── AICity22_Track1_MTMC_Tracking/
    └── train/
        └── S04/
            └── c020/
                └── vdo.avi
```

#### 🏠 Indoor Scenarios (MTMMC Dataset)
```bash
# Download from MTMMC Dataset
# Source: https://sites.google.com/view/mtmmc
# Purpose: Multi-modal camera tracking

# Expected directory structure:
./data/indoor/mtmmc/
└── train/
    └── s01/
        └── c03/
            └── rgb/
```

### 🚀 Launch System

#### Method 1: Using Startup Script (Recommended)
```bash
chmod +x run.sh
./run.sh
```

#### Method 2: Direct Launch
```bash
streamlit run app.py --server.port 8506 --server.address 0.0.0.0
```

### 🌐 Access System
Open your browser and visit: **http://localhost:8506**

## 📁 Project Structure

```
GTR-Bench/
├── 📄 app.py                       # Main Streamlit application
├── 🚀 run.sh                       # Startup script
├── 📋 requirements.txt             # Python dependencies
├── 📖 README.md                    # Project documentation
├── 📊 LICENSE                      # MIT License
│
├── 📁 data/                        # Dataset directory
│   ├── 🏠 indoor/                  # Indoor scenario data
│   │   ├── mtmmc/                  # MTMMC dataset
│   │   └── homography/             # Camera homography data
│   └── 🌆 outdoor/                 # Outdoor scenario data
│       └── cityflow/               # CityFlow dataset
│
├── 📁 eval/                        # Evaluation framework
│   ├── 🐍 eval.py                  # Main evaluation script
│   ├── 📝 eval_type.py             # Evaluation type definitions
│   ├── 📁 prompt/                  # Prompt generation modules
│   │   ├── question_info.py        # Question information
│   │   ├── map_info.py             # Map information
│   │   └── video_info.py           # Video information
│   └── 📁 utils/                   # Evaluation utilities
│       ├── image_utils.py          # Image processing
│       ├── time_utils.py           # Time utilities
│       └── scoring.py              # Scoring algorithms
│
└── 📁 utils/                       # Core utilities
    ├── 📊 data_loader.py           # Data loading and management
    ├── 🎥 video_processor.py       # Video processing utilities
    └── 🎯 scoring.py               # Scoring system
```

## 🎮 Usage Guide

### 👤 Human Assessment

1. **📋 Setup**: Select scene (indoor/outdoor) and task type in the sidebar
2. **🔄 Load Data**: Click "🔄 Load Question Data" to load evaluation cases
3. **👀 Review**: View map and camera images for context
4. **✍️ Answer**: Complete questions and submit responses
5. **📊 Results**: View scoring results and performance metrics

### 🤖 Automated Model Evaluation

1. **🚀 Launch**: Click "🚀 Launch Model Evaluation" in sidebar
2. **⚙️ Configure**: Set model parameters:
   - Model name (e.g., `gpt-4o`, `claude-3-sonnet`)
   - API Key and Base URL
   - Max tokens and temperature
3. **📋 Select Scope**: Choose test scope:
   - **Specific Scene-Task**: Test specific scenario
   - **All Scenes-Tasks**: Comprehensive evaluation
4. **▶️ Start**: Click "🚀 Start Evaluation"
5. **📈 Monitor**: Watch real-time progress and logs
6. **📊 Analyze**: View evaluation results and statistics

### 📈 Result Analysis

1. **📁 Select**: Click "📈 View Evaluation Results"
2. **📄 Choose File**: Select evaluation result JSON file
3. **📊 Statistics**: View overall performance metrics
4. **🔍 Details**: Analyze individual case results
5. **📥 Export**: Download results as CSV for further analysis

## 🔧 Configuration

### 🐍 Environment Setup
- ✅ **Python 3.8+** properly installed
- ✅ **All dependencies** installed via `pip install -r requirements.txt`
- ✅ **Conda environment** activated (if using conda)

### 🔑 API Configuration
- 🔑 **OpenAI-compatible API key** prepared
- 🌐 **Base URL** configured correctly
- ⚙️ **Model parameters** set appropriately:
  - Max tokens: 16384 (recommended)
  - Temperature: 0.1 (for consistent results)

### 📊 Data Configuration
- 📁 **Data files** in correct directories
- ✅ **File formats** verified
- 🔗 **Image/video paths** validated

## 📊 Evaluation Metrics

| Metric | Description | Range | Weight |
|--------|-------------|-------|--------|
| **MCQ Accuracy** | Multiple choice question accuracy | 0-1 | 0.6 |
| **Time IoU** | Time range intersection over union | 0-1 | 0.4 |
| **Overall Score** | Weighted combination of above | 0-1 | - |

### 🎯 Scoring Formula
```
Overall Score = 0.6 × MCQ_Accuracy + 0.4 × Time_IoU
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use GTR-Bench in your research, please cite our paper:

```bibtex
@article{gtr-bench2024,
  title={GTR-Bench: Evaluating Geo-Temporal Reasoning in Vision-Language Models},
  author={Anonymous},
  journal={arXiv preprint},
  year={2024}
}
```

## 🙏 Acknowledgments

- **CityFlow Dataset**: AI City Challenge organizers
- **MTMMC Dataset**: Multi-Target Multi-Modal Camera tracking team
- **Streamlit**: For the excellent web framework

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[Report Bug](https://github.com/X-Luffy/GTR-Bench/issues) · [Request Feature](https://github.com/X-Luffy/GTR-Bench/issues) · [Documentation](https://github.com/X-Luffy/GTR-Bench/wiki)

</div>


