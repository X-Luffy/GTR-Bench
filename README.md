## *GTR-Bench*: Evaluating Geo-Temporal Reasoning in Vision-Language Models
## Abstract
Recently spatial-temporal intelligence of Visual-Language Models (VLMs) has attracted much attention due to its importance for Autonomous
Driving, Embodied AI and General Artificial Intelligence. Existing spatial-temporal benchmarks mainly focus on egocentric perspective reasoning with images/video context, or geographic perspective reasoning with graphics context (eg. a map), thus fail to assess VLMs' geographic spatial-temporal intelligence with both images/video and graphics context, which is important for areas like traffic management and emergency response. To address the gaps, we introduce Geo-Temporal Reasoning benchmark (GTR-Bench), a novel challenge for geographic temporal reasoning of moving targets in a large-scale camera network. GTR-Bench is more challenging as it requires multiple perspective switches between maps and videos, joint reasoning across multiple videos with non-overlapping fields of view, and inference over spatial-temporal regions that are unobserved by any video context. Evaluations of more than 10 popular VLMs on GTR-Bench demonstrate that even the best proprietary model, Gemini-2.5-Pro (34.9\%), significantly lags behind human performance (78.61\%) on geo-temporal reasoning. Moreover, our comprehensive analysis on GTR-Bench reveals three primary deficiencies of current models for geo-temporal reasoning. (1) VLMs' reasoning is impaired by an imbalanced utilization of spatial-temporal context. (2) VLMs are weak in temporal forecasting, which leads to worse performance on temporal-emphasized tasks than on spatial-emphasized tasks. (3) VLMs lack the proficiency to comprehend or align the map data with multi-view video inputs. We believe GTR-Bench offers valuable insights and opens up new opportunities for research and applications in spatial-temporal intelligence. Benchmark and code will be released at https://anonymous.4open.science/r/GTR-Bench-5B76.

## ✨ Key Features

### 🧠 Supported Task Types
- **MotionState**
- **GeoLocation**
- **ArrivalTimeInterval**
- **CausalReordering**
- **TrajectoryForecasting**
- **NextSpotForecasting**
- **MultiTargetTrajectoryForecasting**

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


