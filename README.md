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

## ✨ GTR-Bench

### 🧠 Task Types & Evaluation

GTR-Bench includes **7 task types** across two categories, evaluated using **MCQ Accuracy** or **ST-IoU** metrics:

#### 📋 Basic Tasks (MCQ Accuracy)
- **Geo-Location (GL)**: Infer intermediate locations between start/end points
- **Arrival Time-Interval (ATI)**: Predict time interval of target's arrival at specific location  
- **Motion-State (MS)**: Infer target's motion state at intermediate locations
- **Causal Reordering (CR)**: Determine correct chronological sequence from unordered video clips

#### 🔗 Combinatorial Tasks (ST-IoU)
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


