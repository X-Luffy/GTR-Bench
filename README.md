# GTR-Bench

A comprehensive Streamlit-based assessment system for evaluating human performance on visual reasoning tasks across multiple scenarios and task types.

## 🎯 Features

- **Multi-Scenario Support**: Supports both outdoor (CityFlow) and indoor (MTMMC) scenarios
- **Diverse Task Types**: 7 different reasoning task types including motion, spatial, temporal, and trajectory forecasting
- **Video Frame Extraction**: Automatic extraction of key frames from videos with bounding box visualization
- **Time IoU Calculation**: Advanced time interval overlap calculation for temporal reasoning tasks
- **Real-time Scoring**: Comprehensive scoring system based on accuracy and response time
- **Result Analysis**: Detailed statistics and performance analytics
- **Data Export**: Export assessment results to CSV format

## 📋 Task Types

GTR-Bench includes 7 different reasoning tasks across two complexity levels:

### Basic Tasks
- **Geo-Location (GL)**: Infer intermediate camera locations between start and end points
- **Arrival Time-Interval (ATI)**: Predict arrival time at intermediate locations  
- **Motion-State (MS)**: Determine target's motion state at intermediate locations

### Combinatorial Tasks
- **Causal Reordering (CR)**: Determine correct chronological sequence of camera visits
- **Next Spot Forecasting (NSF)**: Predict next camera location and time interval
- **Trajectory Forecasting (TF)**: Forecast complete future trajectory across multiple cameras
- **Multi-Target Trajectory Forecasting (MTTF)**: Predict meeting point of two targets

**Evaluation Metrics**: Basic tasks use Multiple-Choice Question Accuracy (MCQ Acc), while combinatorial tasks use Spatial-Temporal Intersection over Union (ST-IoU).

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone the Repository
```bash
git clone https://github.com/X-Luffy/GTR-Bench.git
cd GTR-Bench
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Access the Application
Open your browser and navigate to: http://localhost:8501

## 📖 Usage Guide

### 1. Load Assessment Data
- Select scenario (outdoor or indoor) from the left sidebar
- Choose task type from the dropdown menu
- Click "🔄 Load Question Data" button

### 2. Assessment Process
- Review the scenario map and camera images
- Read the question description carefully
- Select the correct answer(s) (single or multiple choice)
- Fill in time information if required
- Click "✅ Submit Answer" button

### 3. View Results
- System displays assessment results and scores
- Compare your answers with ground truth
- Click "📈 View Assessment Results" in sidebar for summary statistics

### 4. Export Results
- Navigate to results summary page
- Click "📥 Export Results" to download CSV file

## 🏆 Evaluation Metrics

GTR-Bench uses two evaluation metrics:

- **MCQ Accuracy**: For basic reasoning tasks (GL, ATI, MS, CR)
- **ST-IoU**: For predictive tasks (NSF, TF, MTTF) - combines spatial correctness and temporal overlap

The ST-IoU metric evaluates both location accuracy and time interval overlap for comprehensive assessment of spatial-temporal reasoning capabilities.

## 📁 Project Structure

```
GTR-Bench/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── data_loader.py         # Data loading utilities
│   ├── video_processor.py     # Video processing utilities
│   └── scoring.py             # Scoring system
├── components/                # UI components
│   ├── __init__.py
│   ├── question_display.py    # Question display components
│   └── result_display.py      # Result display components
└── data/                      # Assessment data
    ├── outdoor/               # Outdoor scenario data
    │   ├── raw_video/         # Raw video files
    │   ├── crop_video/        # Cropped video files
    │   ├── map/               # Map images
    │   └── *.json             # Question data files
    └── indoor/                # Indoor scenario data
        ├── raw_video/         # Raw video files
        ├── crop_video/        # Cropped video files
        ├── map/               # Map images
        └── *.json             # Question data files
```

## 📊 Data Format

The system supports JSON format for question data. Each question contains:
- Scene map path
- Camera image information (video path, frame IDs, bounding boxes)
- Question description
- Answer choices
- Ground truth answers
- Time information (optional)

### Example Question Structure
```json
{
  "cases": [
    {
      "task_id": "NextSpotForecasting",
      "case_id": "WAAGReEpzGHYNLDT2hmsAn",
      "map_image_path": "./map/NextSpotForecasting_map_4_WAAGReEpzGHYNLDT2hmsAn.png",
      "question": "Based on the provided [local map] and [camera information], which camera from the following list will most likely capture the target next?",
      "choices": ["A. c09", "B. c16", "C. c11", "D. c01"],
      "correct_cam_name": ["B. c16"],
      "correct_time_str": ["12:01:18.440-12:01:46.880"],
      "camera_images": [
        {
          "camera_id": "c09",
          "object_id": 4,
          "video_path": "./raw_video/indoor_s01_c09",
          "crop_video_path": "./crop_video/indoor_s01_4_76_83_c09.mp4",
          "frame_ids": [1911, 1941, 1971, 2001, 2031, 2061],
          "bboxes": [[310.07, 274.0, 81.53, 312.23], [522.0, 293.9, 140.1, 317.1], ...],
          "start_timestamp": 76.44,
          "end_timestamp": 82.56
        }
      ]
    }
  ]
}
```


## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup
git clone https://github.com/X-Luffy/GTR-Bench.git
cd GTR-Bench
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and test
4. Commit: `git commit -m "Add: your feature"`
5. Push: `git push origin feature/your-feature`
6. Create a Pull Request

## 📊 Data Download

Due to file size limitations, media files are hosted separately. Download instructions are available in each data directory:
- `data/outdoor/raw_video/README.md`
- `data/outdoor/crop_video/README.md`
- `data/outdoor/map/README.md`
- `data/indoor/raw_video/README.md`
- `data/indoor/crop_video/README.md`
- `data/indoor/map/README.md`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or issues, please open an issue in the GitHub repository.

---

**Note**: This system is designed for research and educational purposes. Ensure compliance with data usage policies and ethical guidelines when using with human subjects.