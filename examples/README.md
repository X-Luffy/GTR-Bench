# GTR-Bench Examples

This directory contains example code and tutorials for using GTR-Bench.

## Structure

```
examples/
├── basic_evaluation/      # Basic evaluation examples
├── custom_models/        # Adding custom VLM models
├── data_preparation/     # Data processing examples
└── analysis/            # Results analysis examples
```

## Quick Start Examples

### 1. Basic Evaluation
```bash
cd basic_evaluation/
python simple_evaluation.py --config ../configs/config.yaml
```

### 2. Custom Model Integration
```bash
cd custom_models/
python custom_model_example.py
```

### 3. Data Preparation
```bash
cd data_preparation/
python prepare_dataset.py --input raw_data/ --output processed_data/
```

## Available Examples

- `basic_evaluation/simple_evaluation.py` - Run a basic evaluation
- `custom_models/custom_model_example.py` - Integrate a custom VLM
- `data_preparation/prepare_dataset.py` - Process raw data
- `analysis/visualize_results.py` - Analyze and visualize results