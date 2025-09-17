# API Documentation

This document describes the API and internal structure of the Human-Level Visual Reasoning Assessment System.

## Core Modules

### `app.py`
Main Streamlit application file containing the user interface and application logic.

#### Key Functions
- `main()`: Application entry point
- `display_current_question()`: Display current assessment question
- `display_question_interface()`: Render question-specific UI components
- `submit_answer()`: Process and score user answers
- `show_result()`: Display assessment results

### `utils/data_loader.py`
Handles loading and parsing of assessment data from JSON files.

#### Key Classes
- `DataLoader`: Main data loading class

#### Key Methods
- `load_data(scene, task_type)`: Load data for specific scene and task type
- `get_cases()`: Retrieve all cases for current dataset

### `utils/video_processor.py`
Manages video processing and frame extraction.

#### Key Classes
- `VideoProcessor`: Video processing utilities

#### Key Methods
- `extract_frames(video_path, frame_ids, bboxes)`: Extract specific frames from video
- `get_video_info(video_path)`: Get video metadata

### `utils/scoring.py`
Implements the scoring system for assessment answers.

#### Key Classes
- `ScoringSystem`: Scoring calculation system

#### Key Methods
- `calculate_score_new(case, user_answers, elapsed_time)`: Calculate comprehensive score
- `calculate_time_iou(user_time, ground_truth_time)`: Calculate time interval overlap

### `components/question_display.py`
UI components for displaying questions and answer interfaces.

#### Key Functions
- `display_option_only_fields()`: Display multiple choice questions
- `display_option_and_time_fields()`: Display questions with time inputs
- `display_trajectory_forecasting_fields()`: Display trajectory prediction interface

### `components/result_display.py`
UI components for displaying assessment results.

#### Key Functions
- `show_results_summary()`: Display overall assessment statistics
- `export_results()`: Export results to CSV format

## Data Structures

### Question Case Structure
```python
{
    "case_id": str,           # Unique identifier
    "task_id": str,           # Task type identifier
    "scene": str,             # Scene description
    "map_image_path": str,    # Path to map image
    "question": str,          # Question text
    "choices": List[str],     # Answer options
    "correct_cam_name": List[str],  # Correct camera answers
    "correct_time_str": List[str],  # Correct time answers
    "camera_images": List[Dict]     # Camera data
}
```

### Camera Image Structure
```python
{
    "camera_id": str,         # Camera identifier
    "object_id": int,         # Object identifier
    "video_path": str,        # Path to video file
    "crop_video_path": str,   # Path to cropped video
    "frame_ids": List[int],   # Frame numbers to extract
    "bboxes": List[List[int]], # Bounding boxes for each frame
    "start_timestamp": float, # Start time in seconds
    "end_timestamp": float    # End time in seconds
}
```

### User Answer Structure
```python
{
    "option_index": int,      # Selected option index
    "options": List[str],     # Selected options
    "time_answers": Dict[str, str],  # Time-based answers
    "trajectory_answers": Dict[str, str]  # Trajectory answers
}
```

### Score Result Structure
```python
{
    "score": float,           # Overall score (0-100)
    "accuracy_score": float,  # Accuracy component
    "time_score": float,      # Time component
    "elapsed_time": float     # Response time in seconds
}
```

## Configuration

### Session State Variables
- `current_task`: Current task identifier
- `current_case_index`: Index of current question
- `user_answers`: User's current answers
- `start_time`: Question start timestamp
- `results`: List of completed assessments
- `data_loader`: DataLoader instance
- `video_processor`: VideoProcessor instance
- `scoring_system`: ScoringSystem instance

### Task Type Mappings
```python
TASK_TYPES = {
    "outdoor": [
        "MotionState", "GeoLocation", "ArrivalTimeInterval",
        "CasualReordering", "TrajectoryForecasting",
        "NextSpotForecasting", "MultiTrajectoryForecasting"
    ],
    "indoor": [
        "MotionState", "GeoLocation", "ArrivalTimeInterval",
        "CasualReordering", "TrajectoryForecasting",
        "NextSpotForecasting", "MultiTrajectoryForecasting"
    ]
}
```

## Error Handling

### Common Error Types
- `FileNotFoundError`: Missing video or image files
- `ValueError`: Invalid time format or data
- `KeyError`: Missing required fields in data
- `Exception`: General application errors

### Error Recovery
- Graceful degradation for missing files
- User-friendly error messages
- Fallback to alternative data sources
- Session state preservation

## Performance Considerations

### Caching Strategy
- Video frames cached in session state
- Map images loaded once per session
- Question data cached after first load

### Optimization Techniques
- Lazy loading of video frames
- Efficient image resizing
- Minimal data transfer
- Responsive UI updates

## Security Considerations

### Data Protection
- No sensitive data in client-side code
- Local file system access only
- Session-based data management
- No external API calls

### Input Validation
- Time format validation
- File path sanitization
- Answer format checking
- Range validation for numeric inputs
