# Data Directory

This directory contains the assessment data for GTR-Bench.

## Data Structure

```
data/
├── outdoor/                    # Outdoor scenario (CityFlow) data
│   ├── raw_video/             # Raw video files (excluded from Git)
│   ├── crop_video/            # Cropped video files (excluded from Git)
│   ├── map/                   # Map images (excluded from Git)
│   └── *.json                 # Question data files
├── indoor/                     # Indoor scenario (MTMMC) data
│   ├── raw_video/             # Raw video files (excluded from Git)
│   ├── crop_video/            # Cropped video files (excluded from Git)
│   ├── map/                   # Map images (excluded from Git)
│   └── *.json                 # Question data files
├── human_level.csv            # Assessment results
└── Task_level_detailed.csv    # Task-level statistics
```

## Data Files

### Question Data (JSON files)
- **outdoor_*.json**: Outdoor scenario question data
- **indoor_*.json**: Indoor scenario question data

Each JSON file contains:
- Question descriptions
- Answer choices
- Ground truth answers
- Camera information
- Video and image paths

### Media Files (Excluded from Git)
Due to file size limitations, the following directories are excluded from the Git repository:
- `raw_video/`: Original video files (~16GB total)
- `crop_video/`: Cropped video segments (~2GB total)
- `map/`: Map images (~100MB total)

## Obtaining the Data

### Option 1: Download from Original Sources
1. **CityFlow Dataset**: Download from [AICity Challenge](https://www.aicitychallenge.org/)
2. **MTMMC Dataset**: Download from the original MTMMC dataset

### Option 2: Use Sample Data
For testing purposes, you can:
1. Create sample video files
2. Use placeholder images
3. Modify the JSON files to point to your local media files

### Option 3: Contact the Authors
For access to the processed dataset used in this research, please contact the authors.

## Data Format

### Video Files
- **Raw videos**: `.avi` format, typically 30fps
- **Cropped videos**: `.mp4` format, containing specific object tracks

### Image Files
- **Map images**: `.png` format, showing camera locations and scene layout

### JSON Structure
```json
{
  "cases": [
    {
      "case_id": "unique_identifier",
      "task_id": "TaskType",
      "scene": "Scene description",
      "map_image_path": "./map/image.png",
      "question": "Question text",
      "choices": ["Option1", "Option2", "Option3", "Option4"],
      "correct_cam_name": ["CorrectAnswer"],
      "correct_time_str": ["HH:MM:SS.mmm"],
      "camera_images": [
        {
          "camera_id": "c01",
          "object_id": 123,
          "video_path": "./raw_video/video.avi",
          "crop_video_path": "./crop_video/cropped.mp4",
          "frame_ids": [100, 150, 200],
          "bboxes": [[x1, y1, x2, y2], ...],
          "start_timestamp": 10.5,
          "end_timestamp": 15.2
        }
      ]
    }
  ]
}
```

## Setup Instructions

1. **Clone the repository** (without data files)
2. **Download or prepare media files** according to your needs
3. **Place media files** in the appropriate directories:
   - Raw videos → `data/outdoor/raw_video/` and `data/indoor/raw_video/`
   - Cropped videos → `data/outdoor/crop_video/` and `data/indoor/crop_video/`
   - Map images → `data/outdoor/map/` and `data/indoor/map/`
4. **Verify file paths** in JSON files match your local setup
5. **Run the application** with `streamlit run app.py`

## File Size Information

- **Total data size**: ~19GB
- **Raw videos**: ~16GB (outdoor: 8.5GB, indoor: 7.9GB)
- **Cropped videos**: ~2GB (outdoor: 763MB, indoor: 1.2GB)
- **Map images**: ~100MB
- **JSON files**: ~50MB

## Notes

- The JSON files contain relative paths to media files
- Ensure all referenced files exist in the correct locations
- Video files are required for the full assessment experience
- Map images are required for scene visualization
- The system will work with sample data for testing purposes
