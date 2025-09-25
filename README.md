# GTR-Bench: Human-Level Visual Reasoning Evaluation System

A comprehensive visual reasoning evaluation platform based on Streamlit, supporting both human assessment and automated model evaluation.

## 🎯 Project Overview

GTR-Bench is a comprehensive visual reasoning evaluation platform designed to assess model capabilities in complex visual scenarios. The system supports two evaluation modes:

1. **Human Assessment**: Manual evaluation through web interface to establish human baselines
2. **Automated Model Evaluation**: Automatic evaluation of various visual reasoning models through API calls

## ✨ Key Features

### 🧠 Supported Task Types
- **MotionState**: Motion state reasoning
- **GeoLocation**: Geographic location reasoning  
- **ArrivalTimeInterval**: Arrival time interval reasoning
- **CausalReordering**: Causal reordering reasoning
- **TrajectoryForecasting**: Trajectory forecasting
- **NextSpotForecasting**: Next spot forecasting
- **MultiTargetTrajectoryForecasting**: Multi-target trajectory forecasting

### 🌍 Supported Data Scenarios
- **Indoor**: Indoor scenarios
- **Outdoor**: Outdoor scenarios

### 🤖 Model Evaluation Features
- OpenAI-compatible API interface support
- Real-time progress monitoring
- Automatic result analysis and visualization
- Support for batch evaluation and single case testing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit
- OpenCV
- PIL/Pillow
- NumPy
- Pandas

### Data Preparation

Before using GTR-Bench, you need to download and prepare the required datasets:

#### 1. Download CityFlow Dataset (Outdoor Scenarios)
- **Source**: [AI City Challenge](https://www.aicitychallenge.org/)
- **Purpose**: Outdoor scenario data for vehicle tracking and re-identification
- **Download**: Visit the official website and download the CityFlow dataset
- **Extract**: Place the extracted data in `./data/outdoor/cityflow/` directory
- **Expected Structure**: `./data/outdoor/cityflow/AICity22_Track1_MTMC_Tracking/train/S04/c020/vdo.avi`

#### 2. Download MTMMC Dataset (Indoor Scenarios)
- **Source**: [MTMMC Dataset](https://sites.google.com/view/mtmmc)
- **Purpose**: Indoor scenario data for multi-modal camera tracking
- **Download**: Visit the official website and download the MTMMC dataset
- **Extract**: Place the extracted data in `./data/indoor/mtmmc/` directory
- **Expected Structure**: `./data/indoor/mtmmc/train/s01/c03/rgb`

### Installation
```bash
pip install -r requirements.txt
```

### Launch System
```bash
# Method 1: Using startup script
chmod +x run.sh
./run.sh

# Method 2: Direct launch
streamlit run app.py --server.port 8505
```

### Access System
Open your browser and visit: `http://localhost:8505`

## 📁 Project Structure

```
├── app.py                          # Main application file
├── run.sh                          # Startup script
├── requirements.txt                 # Dependencies list
├── README.md                       # Project documentation
├── README_EVAL_FEATURE.md          # Evaluation feature documentation
├── .gitignore                      # Git ignore file
├── data/                           # Data directory
│   ├── indoor/                     # Indoor scenario data
│   └── outdoor/                    # Outdoor scenario data
├── eval/                           # Evaluation module
│   ├── eval.py                     # Main evaluation script
│   ├── eval_type.py                # Evaluation type definitions
│   ├── run_full_evaluation.sh      # Full evaluation script
│   ├── results/                    # Evaluation results directory
│   └── prompt/                     # Prompt modules
│       ├── question_info.py        # Question information
│       ├── map_info.py             # Map information
│       └── video_info.py           # Video information
├── utils/                          # Utility modules
│   ├── data_loader.py              # Data loader
│   ├── video_processor.py          # Video processor
│   └── scoring.py                  # Scoring system
└── components/                     # UI components
    ├── question_display.py         # Question display component
    └── result_display.py           # Result display component
```

## 🎮 Usage Guide

### Human Assessment
1. Select scene and task type in the sidebar
2. Click "🔄 Load Question Data"
3. View map and camera images
4. Answer questions and submit
5. View scoring results

### Automated Model Evaluation
1. Click "🚀 Launch Model Evaluation"
2. Configure model parameters (API Key, Base URL, etc.)
3. Select test scope and number of cases
4. Click "🚀 Start Evaluation"
5. Monitor evaluation progress in real-time
6. View evaluation results

### Result Analysis
1. Click "📈 View Evaluation Results"
2. Select evaluation result file
3. View statistical information and detailed results
4. Analyze model performance

## 🔧 Configuration

### Environment Setup
- Ensure Python environment is properly installed
- Install all required dependencies
- Configure conda environment (if needed)

### API Configuration
- Prepare OpenAI-compatible API key
- Configure correct Base URL
- Set appropriate model parameters

### Data Configuration
- Ensure data files are in the correct directories
- Check data file formats are correct
- Verify image and video file paths

## 📊 Evaluation Metrics

The system supports multiple evaluation metrics:

- **MCQ Accuracy**: Multiple choice question accuracy
- **Time IoU**: Time range intersection over union
- **Overall Score**: Comprehensive score


