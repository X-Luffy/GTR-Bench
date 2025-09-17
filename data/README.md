# GTR-Bench Data Organization

This directory contains all data for the GTR-Bench benchmark.

## Directory Structure

```
data/
├── raw/                    # Original, unprocessed datasets
├── processed/              # Cleaned and formatted data
├── annotations/            # Ground truth labels and metadata
├── splits/                # Train/validation/test split definitions
├── samples/               # Small sample datasets for testing
└── tasks/                 # Task-specific data organization
    ├── spatial_reasoning/
    ├── spatial_understanding/
    ├── spatial_navigation/
    └── object_relations/
```

## Data Format Guidelines

### Images
- Format: JPG, PNG (recommended: JPG for photographs, PNG for diagrams)
- Resolution: Minimum 224x224, recommended 512x512 or higher
- Naming: `{task}_{split}_{id}.{ext}`

### Annotations
- Format: JSON for structured data, CSV for tabular data
- Structure: See `annotations/annotation_schema.json` for format specification
- Naming: `{task}_{split}_annotations.json`

### Data Splits
- Format: Text files with one sample ID per line
- Files: `train_ids.txt`, `val_ids.txt`, `test_ids.txt`
- Location: `splits/{task}/`

## Usage

1. Place raw data in the `raw/` directory
2. Run preprocessing scripts to generate `processed/` data
3. Ensure annotations follow the schema in `annotations/`
4. Use predefined splits or create custom ones in `splits/`

## Sample Data

The `samples/` directory contains small datasets for:
- Testing the evaluation pipeline
- Development and debugging
- Demonstration purposes

## Adding New Data

1. Follow the naming conventions
2. Update the annotation schema if needed
3. Create appropriate data splits
4. Document any preprocessing steps
5. Add to the task-specific directory structure