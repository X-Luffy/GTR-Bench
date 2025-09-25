# GTR-Bench Evaluation System

This directory contains the evaluation system for GTR-Bench, a comprehensive benchmark for visual reasoning models.

## Directory Structure

```
eval/
├── eval.py                    # Main evaluation script
├── eval_type.py              # Evaluation type definitions
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── README_EVALUATION.md     # Detailed evaluation guide
├── run_full_evaluation.sh   # Full evaluation script (420 cases)
├── prompt/                  # Prompt generation modules
│   ├── map_info.py         # Map information handling
│   ├── question_info.py    # Question and rule definitions
│   └── video_info.py       # Video and camera information
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── ARIAL.TTF          # Font file for image processing
│   ├── image_utils.py     # Image processing utilities
│   ├── metric.py          # Metric calculation functions
│   ├── model_api.py       # Model API interface
│   ├── scoring.py         # Scoring system
│   └── time_utils.py      # Time-related utilities
└── results/                # Evaluation results
    ├── *.json             # Consolidated result files
    └── prompt/            # Individual prompt files
```

## Quick Start

### Full Evaluation (420 cases)
```bash
./run_full_evaluation.sh
```

### Custom Evaluation
```bash
python eval.py \
    --model "model_name" \
    --api-key "api_key" \
    --base-url "base_url" \
    --data-dir "../data" \
    --result-dir "./results" \
    --max-cases 10 \
    --verbose
```

## Key Features

- **Multi-task Evaluation**: 7 task types (MotionState, GeoLocation, ArrivalTimeInterval, NextSpotForecasting, TrajectoryForecasting, MultiTargetTrajectoryForecasting, CausalReordering)
- **Flexible Model Support**: OpenAI API-compatible models
- **Comprehensive Metrics**: Score, MCQ accuracy, Time IoU
- **Consolidated Results**: Single JSON file per model with all test cases
- **Prompt Management**: Individual prompt files with model names

## Output Files

- **Results**: `results/{model_name}_{timestamp}.json` - Consolidated results
- **Prompts**: `results/prompt/prompt_{model_name}_{case_id}_{task_id}_{timestamp}.json` - Individual prompts

## Configuration

Edit `run_full_evaluation.sh` to modify:
- API key and base URL
- Model name
- Data and result directories

## Dependencies

```bash
pip install -r requirements.txt
```

## Documentation

See `README_EVALUATION.md` for detailed usage instructions and examples.