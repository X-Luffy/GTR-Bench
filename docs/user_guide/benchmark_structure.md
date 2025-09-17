# GTR-Bench Structure Guide

This document explains the organization and structure of the GTR-Bench benchmark.

## Directory Structure

```
GTR-Bench/
├── data/                     # Data organization
│   ├── raw/                  # Raw, unprocessed data
│   ├── processed/            # Processed and formatted data
│   ├── annotations/          # Annotation files (JSON, CSV)
│   ├── splits/              # Train/val/test split definitions
│   ├── samples/             # Small sample datasets for testing
│   └── tasks/               # Task-specific data organization
│       ├── spatial_reasoning/
│       ├── spatial_understanding/
│       ├── spatial_navigation/
│       └── object_relations/
├── src/                     # Source code
│   ├── gtr_bench/          # Main benchmark package
│   │   ├── tasks/          # Task implementations
│   │   ├── metrics/        # Evaluation metrics
│   │   └── datasets/       # Dataset loaders
│   ├── evaluation/         # Evaluation framework
│   ├── models/            # Model wrappers and interfaces
│   ├── data_processing/   # Data processing utilities
│   └── utils/             # General utilities
├── configs/               # Configuration files
│   ├── models/           # Model configurations
│   ├── tasks/            # Task configurations
│   ├── evaluation/       # Evaluation configurations
│   └── datasets/         # Dataset configurations
├── experiments/           # Experiment management
│   ├── runs/             # Individual experiment runs
│   ├── logs/             # Experiment logs
│   └── checkpoints/      # Model checkpoints
├── results/              # Results and analysis
│   ├── outputs/          # Raw evaluation outputs
│   ├── analysis/         # Analysis scripts and notebooks
│   ├── reports/          # Generated reports
│   └── leaderboard/      # Leaderboard data
├── scripts/              # Utility scripts
│   ├── data_processing/  # Data preparation scripts
│   ├── evaluation/       # Evaluation runner scripts
│   ├── analysis/         # Analysis and visualization scripts
│   └── setup/            # Setup and installation scripts
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data and fixtures
├── docs/                 # Documentation
│   ├── api/              # API documentation
│   ├── user_guide/       # User guides
│   ├── developer_guide/  # Developer documentation
│   └── assets/           # Documentation assets
└── examples/             # Example usage and tutorials
    ├── basic_evaluation/
    ├── custom_models/
    └── data_preparation/
```

## Key Components

### Data Organization (`data/`)

- **raw/**: Store original, unmodified datasets
- **processed/**: Clean, formatted data ready for evaluation
- **annotations/**: Ground truth labels and metadata
- **splits/**: Predefined train/validation/test splits
- **tasks/**: Task-specific data organization

### Source Code (`src/`)

- **gtr_bench/**: Core benchmark library
- **evaluation/**: Evaluation pipeline and runners
- **models/**: Model wrappers for different VLM architectures
- **data_processing/**: Data loading and preprocessing utilities

### Configuration (`configs/`)

YAML configuration files for:
- Model settings and hyperparameters
- Task definitions and parameters
- Evaluation protocols
- Dataset specifications

### Experiments (`experiments/`)

- **runs/**: Individual experiment outputs
- **logs/**: Detailed execution logs
- **checkpoints/**: Model states and intermediate results

### Results (`results/`)

- **outputs/**: Raw evaluation results (JSON, CSV)
- **analysis/**: Analysis notebooks and visualizations
- **reports/**: Formatted reports and summaries
- **leaderboard/**: Performance rankings and comparisons

## File Naming Conventions

### Data Files
- Images: `{task}_{split}_{id}.{ext}` (e.g., `spatial_reasoning_train_001.jpg`)
- Annotations: `{task}_{split}_annotations.json`
- Splits: `{task}_{split}_ids.txt`

### Configuration Files
- Models: `{model_name}.yaml` (e.g., `clip_large.yaml`)
- Tasks: `{task_name}.yaml` (e.g., `spatial_reasoning.yaml`)

### Results Files
- Outputs: `{model}_{task}_{timestamp}.json`
- Reports: `{experiment_name}_report_{date}.pdf`

### Code Files
- Tasks: `{task_name}_task.py`
- Metrics: `{metric_name}.py`
- Models: `{model_name}_wrapper.py`

## Adding New Components

### Adding a New Task
1. Create task configuration in `configs/tasks/{task_name}.yaml`
2. Implement task class in `src/gtr_bench/tasks/{task_name}_task.py`
3. Add data directory in `data/tasks/{task_name}/`
4. Update task registry in `src/gtr_bench/tasks/__init__.py`

### Adding a New Model
1. Create model configuration in `configs/models/{model_name}.yaml`
2. Implement model wrapper in `src/models/{model_name}_wrapper.py`
3. Add example usage in `examples/custom_models/`

### Adding a New Metric
1. Implement metric function in `src/gtr_bench/metrics/{metric_name}.py`
2. Register in `src/gtr_bench/metrics/__init__.py`
3. Add tests in `tests/unit/test_metrics.py`

## Best Practices

1. **Version Control**: Use Git LFS for large data files
2. **Documentation**: Document all configuration options
3. **Testing**: Add unit tests for new components
4. **Reproducibility**: Pin dependency versions and use seeds
5. **Modularity**: Keep components loosely coupled and configurable