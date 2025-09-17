# GTR-Bench

A comprehensive benchmark for evaluating the generalized spatial intelligence of Vision-Language Models (VLMs).

## Overview

GTR-Bench provides a standardized evaluation framework for assessing how well Vision-Language Models understand and reason about spatial relationships, object positioning, navigation, and spatial transformations in visual scenes.

## Key Features

- **Comprehensive Task Coverage**: Spatial reasoning, understanding, navigation, and object relations
- **Standardized Evaluation**: Consistent metrics and protocols across tasks
- **Modular Design**: Easy integration of custom models and datasets
- **Extensible Framework**: Plugin architecture for new tasks and metrics
- **Reproducible Results**: Configuration-driven experiments with version control

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/X-Luffy/GTR-Bench.git
cd GTR-Bench

# Run the installation script
./scripts/setup/install.sh

# Or install manually
pip install -r requirements.txt
pip install -e .
```

### Basic Usage

```python
from gtr_bench import GTRBenchmark

# Initialize benchmark
benchmark = GTRBenchmark(config_path="configs/config.yaml")

# Run evaluation
results = benchmark.evaluate(
    model_name="your_model",
    tasks=["spatial_reasoning", "spatial_understanding"]
)

# View results
print(results.summary())
```

### Command Line Interface

```bash
# Run all tasks
python scripts/evaluation/run_benchmark.py --config configs/config.yaml

# Run specific task
python scripts/evaluation/run_benchmark.py --task spatial_reasoning

# Custom model configuration
python scripts/evaluation/run_benchmark.py --model-config configs/models/custom_model.yaml
```

## Benchmark Structure

```
GTR-Bench/
├── data/                     # Dataset organization
│   ├── raw/                  # Original datasets
│   ├── processed/            # Formatted data
│   ├── annotations/          # Ground truth labels
│   └── tasks/               # Task-specific data
├── src/                     # Source code
│   └── gtr_bench/          # Main package
│       ├── tasks/          # Task implementations
│       ├── metrics/        # Evaluation metrics
│       └── datasets/       # Data loaders
├── configs/                 # Configuration files
├── experiments/             # Experiment tracking
├── results/                 # Evaluation outputs
├── scripts/                 # Utility scripts
├── docs/                   # Documentation
└── examples/               # Usage examples
```

## Tasks

### 1. Spatial Reasoning
Evaluate model's ability to reason about spatial relationships between objects.
- Relative positioning (left/right, above/below)
- Distance estimation
- Spatial transformations

### 2. Spatial Understanding
Assess comprehension of spatial layouts and object arrangements.
- Scene composition
- Object arrangement patterns
- Spatial groupings

### 3. Spatial Navigation
Test navigation and path-finding capabilities.
- Route planning
- Landmark recognition
- Direction following

### 4. Object Relations
Examine understanding of object interactions and relationships.
- Containment relationships
- Support relationships
- Proximity relationships

## Configuration

GTR-Bench uses YAML configuration files for easy customization:

```yaml
# config.yaml
data:
  root_dir: "./data"
  tasks: ["spatial_reasoning", "spatial_understanding"]

model:
  name: "clip_large"
  batch_size: 32

evaluation:
  metrics: ["accuracy", "spatial_accuracy"]
  output_dir: "./results"
```

## Adding New Components

### New Task
1. Create task configuration: `configs/tasks/new_task.yaml`
2. Implement task class: `src/gtr_bench/tasks/new_task.py`
3. Add task data: `data/tasks/new_task/`

### New Model
1. Create model wrapper: `src/models/new_model.py`
2. Add configuration: `configs/models/new_model.yaml`
3. Test integration: `examples/custom_models/`

### New Metric
1. Implement metric: `src/gtr_bench/metrics/new_metric.py`
2. Register in metric registry
3. Add unit tests

## Documentation

- [Benchmark Structure Guide](docs/user_guide/benchmark_structure.md)
- [API Documentation](docs/api/)
- [Developer Guide](docs/developer_guide/)
- [Examples](examples/)

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/developer_guide/contributing.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use GTR-Bench in your research, please cite:

```bibtex
@misc{gtr-bench,
  title={GTR-Bench: A Benchmark for Evaluating Generalized Spatial Intelligence of Vision-Language Models},
  author={GTR-Bench Team},
  year={2024},
  url={https://github.com/X-Luffy/GTR-Bench}
}
```

## Contact

For questions and issues, please:
- Open an issue on GitHub
- Check the documentation
- Join our community discussions
