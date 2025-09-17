# Human-Level Visual Reasoning Assessment System

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

### Outdoor Scenario (CityFlow)
- **MotionState**: Motion state reasoning - multiple choice questions
- **GeoLocation**: Geographic location reasoning - multiple choice questions  
- **ArrivalTimeInterval**: Arrival time interval reasoning - multiple choice questions
- **CasualReordering**: Causal reordering reasoning - multiple choice questions
- **TrajectoryForecasting**: Trajectory prediction - predict two cameras + time ranges
- **NextSpotForecasting**: Next location forecasting - multiple choice + time range fill-in
- **MultiTrajectoryForecasting**: Multi-trajectory forecasting - multiple choice + time range fill-in

### Indoor Scenario (MTMMC)
- **MotionState**: Motion state reasoning - multiple choice questions
- **GeoLocation**: Geographic location reasoning - multiple choice questions
- **ArrivalTimeInterval**: Arrival time interval reasoning - multiple choice questions
- **CasualReordering**: Causal reordering reasoning - multiple choice questions
- **TrajectoryForecasting**: Trajectory prediction - predict two cameras + time ranges
- **NextSpotForecasting**: Next location forecasting - multiple choice + time range fill-in
- **MultiTrajectoryForecasting**: Multi-trajectory forecasting - multiple choice + time range fill-in

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone the Repository
```bash
git clone <repository-url>
cd human_level
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

### Score Calculation
- **Accuracy Score** (70% weight): Based on correctness of option answers and time answers
- **Time Score** (30% weight): Based on response time, faster responses receive higher scores

### Time IoU Calculation
For temporal reasoning tasks, the system calculates time IoU between user answers and ground truth:
- Supports time range format: "HH:MM:SS.mmm-HH:MM:SS.mmm"
- Supports single time point format: "HH:MM:SS.mmm"
- Allows 0.5-second error tolerance

## 📁 Project Structure

```
human_level/
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
      "case_id": "unique_case_id",
      "task_id": "MotionState",
      "scene": "Track 4",
      "map_image_path": "./map/MotionState_map_259_xxx.png",
      "question": "What is the motion state of the target?",
      "choices": ["Walking", "Running", "Standing", "Sitting"],
      "correct_cam_name": ["Walking"],
      "camera_images": [
        {
          "camera_id": "c03",
          "object_id": 259,
          "video_path": "./raw_video/outdoor_S04_c020.avi",
          "crop_video_path": "./crop_video/outdoor_S04_259_52_59_c020.mp4",
          "frame_ids": [263, 276, 289],
          "bboxes": [[x1, y1, x2, y2], ...],
          "start_timestamp": 10.5,
          "end_timestamp": 15.2
        }
      ]
    }
  ]
}
```

## ⚠️ Important Notes

1. **File Paths**: Ensure video file paths are correct and accessible
2. **Time Format**: Time must be entered in strict "HH:MM:SS.mmm" format
3. **Performance**: System automatically caches video frames for improved performance
4. **Session Management**: Assessment results are saved in session; refreshing the page will lose current progress
5. **Browser Compatibility**: Recommended to use modern browsers (Chrome, Firefox, Safari, Edge)

## 🛠️ Technical Stack

- **Frontend Framework**: Streamlit
- **Image Processing**: OpenCV, Pillow
- **Data Processing**: Pandas, NumPy
- **Video Processing**: OpenCV
- **Scoring Algorithm**: Custom scoring system with IoU calculations

## 🔧 Development

### Adding New Task Types
1. Update task type mappings in `app.py`
2. Add corresponding question display logic
3. Update scoring system if needed
4. Add sample data in appropriate scenario folder

### Customizing Scoring
Modify the scoring logic in `utils/scoring.py` to adjust:
- Accuracy vs. time score weights
- Time IoU tolerance
- Scoring thresholds

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