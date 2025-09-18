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

## 📋 Supported Task Types

| Task Type | Task Name | Task Definition | Metric |
|-----------|-----------|-----------------|---------|
| **Basic** | **Geo-Location (GL)** | Given the starting and ending locations of a target, infer the intermediate locations the target passes through. *Example: Based on the provided [start video] and [end video], infer which camera the target passed through between the start point (c016, 12:00:10-12:00:22) and end point (c018, 12:00:37-12:00:42).* | MCQ Acc |
| **Basic** | **Arrival Time-Interval (ATI)** | Given the starting point, ending point, and intermediate location, infer when the target will arrive at specific intermediate interval. *Example: Based on the provided [start video] (c018, 12:00:37-12:00:42) and [end video] (c020, 12:00:43-12:00:50), and knowing the target passed through camera c019, infer when the target arrived at the intermediate camera.* | MCQ Acc |
| **Basic** | **Motion-State (MS)** | Given the starting point, ending point, and intermediate location, infer the reasonable motion state of the target at intermediate locations. *Example: Based on the provided [start video] (c016, 12:00:10-12:00:22) and [end video] (c018, 12:00:37-12:00:42), and the intermediate camera c017 infer the target's motion state during the intermediate time period.* | MCQ Acc |
| **Combinatorial** | **Causal Reordering (CR)** | Given a set of unordered video clips from different cameras and a map, determine the correct chronological sequence of cameras the target passed through. *Example: Based on the provided [local map] and [videos], analyze the target's activity trajectory. Please infer the correct order in which the target passed through these cameras.* | MCQ Acc |
| **Combinatorial** | **Next Spot Forecasting (NSF)** | Given the target's last observed appearance in a single camera video and a map, predict the most probable next camera location and the corresponding time interval of appearance. *Example: Based on the provided [local map] and [video], which camera from the following list will likely capture the target next? You need to select one option as the answer and infer a time range.* | ST-IoU |
| **Combinatorial** | **Trajectory Forecasting (TF)** | Building upon multiple historical observations across several cameras, predict the target's complete future trajectory by forecasting the sequence of cameras it will pass through. *Example: Based on the provided [local map] and [videos], predict the next two cameras that the target will likely pass through. You need to select a correct option sequence and infer a time range sequence simultaneously.* | ST-IoU |
| **Combinatorial** | **Multi-Target Trajectory Forecasting (MTTF)** | This extends single-target prediction by requiring the model to forecast the future meeting point (location and time) of two distinct targets. *Example: Based on the provided [local map] and [videos] showing the movement trajectories of two [Target], predict where and when these [Target] will most likely meet.* | ST-IoU |

GTR-Bench is divided into basic and combinatorial level, evaluated by either Multiple-Choice Question Accuracy (MCQ Acc) or Spatial-Temporal Intersection over Union (ST-IoU).

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

## 🏆 Scoring System

### Metric Design
We employ two primary metrics to evaluate model performance: standard accuracy for multiple-choice questions (MCQ) and a novel Spatial-Temporal Intersection over Union (ST-IoU) for predictive tasks. For the basic tasks and the CR task, which are formatted as MCQs, we report the accuracy. For predictive tasks (NSF, TF, and MTTF), we use ST-IoU to provide a more comprehensive assessment. The ST-IoU metric is designed to holistically evaluate a model's spatial-temporal prediction capabilities by jointly considering the correctness of the predicted location and the overlap of the predicted time interval. For a given prediction i, the ST-IoU is calculated as follows:

```
ST-IoU = (1/N) * Σ(i=1 to N) I(C_pi = C_gti) * |T_pi ∩ T_gti| / |T_pi ∪ T_gti|
```

where N is the total number of predictions, I(·) is the indicator function which equals 1 if the predicted camera C_pi matches the ground truth camera C_gti and 0 otherwise. T_pi and T_gti represent the predicted and ground-truth time intervals, respectively, and the fraction calculates their temporal Intersection over Union.

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
      "task_id": "MotionState",
      "case_id": "KehMGKMHJJ2RiWzTpeXKYQ",
      "map_image_path": "./map/MotionState_map_259_KehMGKMHJJ2RiWzTpeXKYQ.png",
      "question": "Based on the provided [start video] (c016, 12:00:10-12:00:22) and [end video] (c018, 12:00:37-12:00:42), and the intermediate camera c017, infer the target's motion state during the intermediate time period.",
      "choices": ["Walking", "Running", "Standing", "Sitting"],
      "correct_cam_name": ["Walking"],
      "correct_time_str": ["12:00:25.000-12:00:30.000"],
      "camera_images": [
        {
          "camera_id": "c03",
          "object_id": 259,
          "video_path": "./raw_video/outdoor_S04_c020.avi",
          "crop_video_path": "./crop_video/outdoor_S04_259_52_59_c020.mp4",
          "frame_ids": [263, 276, 289, 302, 315],
          "bboxes": [[304.0, 760.0, 84.0, 65.0], [330.0, 765.0, 101.0, 83.0], ...],
          "start_timestamp": 10.5,
          "end_timestamp": 15.2
        }
      ]
    }
  ]
}
```


## 📄 License

This project is for research purposes only.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For questions or issues, please open an issue in the GitHub repository.

---

**Note**: This system is designed for research and educational purposes. Ensure compliance with data usage policies and ethical guidelines when using with human subjects.