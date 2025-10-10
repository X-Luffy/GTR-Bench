# GTR-Bench: Evaluating Geo-Temporal Reasoning in Vision-Language Models

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 Abstract

Enhancing the spatial intelligence of Visual-Language Models (VLMs) is critical for applications like autonomous driving and embodied AI, yet existing benchmarks fail to assess complex, real-world reasoning. Current benchmarks are often confined to single or a few camera views, with limited perspective changes and understanding tasks for observed scenarios. To address these gaps, we introduce the Geo-Temporal Reasoning benchmark (GTR-Bench), a novel challenge to evaluate the spatial intelligence of VLMs. It features a hierarchical suite of tasks grounded in real-world multi-camera networks, compelling models to reason with absolute time information and infer unobserved states with multiple perspective changes. Our evaluation based on more than 10 popular VLMs reveals a critical performance gap, with even the best proprietary model, Gemini-2.5-Pro, achieving only 34.9\% accuracy. Our analysis attributes this poor performance to three primary deficiencies in current models. (1) VLMs' reasoning is impaired by an imbalanced utilization of spatial-temporal context. (2) VLMs are weak in temporal forecasting, which leads to worse performance on spatial-temporal prediction tasks than on spatial reasoning tasks. (3) VLMs lack the proficiency to comprehend or align the map data with multi-view video inputs. We believe that GTR-Bench offers valuable insights and helps bridge the gap between VLMs and generalized spatial intelligence.

## ✨ GTR-Bench

![task fig](msic/task_fig.png)

### 🧠 Task Types & Evaluation

GTR-Bench includes **7 task types** across two categories, evaluated using **MCQ Accuracy** or **ST-IoU** metrics:

#### 📋 Basic Tasks
- **Geo-Location (GL)**: Infer intermediate locations between start/end points
- **Arrival Time-Interval (ATI)**: Predict time interval of target's arrival at specific location  
- **Motion-State (MS)**: Infer target's motion state at intermediate locations

#### 🔗 Combinatorial Tasks
- **Causal Reordering (CR)**: Determine correct chronological sequence from unordered video clips
- **Next Spot Forecasting (NSF)**: Predict next camera location and time interval
- **Trajectory Forecasting (TF)**: Forecast complete future trajectory sequence
- **Multi-Target Trajectory Forecasting (MTTF)**: Predict meeting point of two targets

#### 🎯 Evaluation Metrics
- **MCQ Accuracy**: Binary score (0/1) for basic tasks
- **ST-IoU**: Continuous score (0-1) for forecasting tasks, calculated as `MCQ_Accuracy × Time_IoU`
- **Scoring Logic**: MCQ must be correct to receive any score; time precision determines final score for forecasting tasks

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
│   │   └── homography/             # Indoor Camera homography data
│   └── 🌆 outdoor/                 # Outdoor scenario data
│       └── cityflow/               # CityFlow dataset
│
├── 📁 eval/                        # Evaluation framework
│   ├── 🐍 eval.py                  # Main evaluation script
│   ├── 📝 eval_type.py             # Evaluation type definitions
│   ├── 📁 prompt/                  # Benchmark Prompt Template
│   │   ├── question_info.py        # Question Prompt Template
│   │   ├── map_info.py             # Map Prompt Template
│   │   └── video_info.py           # Video Prompt Template
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


## 🙏 Acknowledgments

- **CityFlow Dataset**: AI City Challenge organizers
- **MTMMC Dataset**: Multi-Target Multi-Modal Camera tracking team
- **Streamlit**: For the excellent web framework


</div>


