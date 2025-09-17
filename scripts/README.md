# Scripts Directory

This directory contains utility scripts used for data processing, validation, and maintenance tasks during the development of the Human-Level Visual Reasoning Assessment System.

## Scripts Overview

### Data Processing Scripts
- **`process_data.py`**: Main data processing script for converting absolute paths to relative paths and organizing video files
- **`rename_and_clean.py`**: Script for renaming files and cleaning JSON data according to new naming conventions
- **`restore_paths.py`**: Utility to restore original file paths from backup data

### Validation Scripts
- **`check_duplicates.py`**: Check for duplicate entries in the dataset
- **`detailed_check.py`**: Comprehensive validation of data integrity
- **`simple_check.py`**: Basic data validation checks
- **`verify_check.py`**: Verification of data processing results

### Debugging Scripts
- **`find_unprocessed.py`**: Find entries that were not properly processed
- **`fix_incorrect_paths.py`**: Fix incorrectly processed file paths
- **`fix_wrong_relative_paths.py`**: Correct relative path issues
- **`test_regex.py`**: Test regular expressions used in path processing

## Usage

These scripts were used during the development and data preparation phase. They are provided for reference and potential future maintenance tasks.

### Running Scripts
```bash
# Navigate to the scripts directory
cd scripts/

# Run a specific script
python script_name.py
```

### Important Notes
- These scripts were designed for the specific data structure and naming conventions used in this project
- Always backup your data before running any processing scripts
- Some scripts may require specific file paths to be updated for your environment

## Script Dependencies

Most scripts require the following Python packages:
- `json`
- `os`
- `re`
- `shutil`
- `glob`
- `pandas` (for some validation scripts)

## Data Processing Workflow

The typical workflow used during development was:

1. **Initial Processing**: `process_data.py` - Convert absolute paths to relative paths
2. **Validation**: `check_duplicates.py`, `detailed_check.py` - Validate data integrity
3. **Renaming**: `rename_and_clean.py` - Apply new naming conventions
4. **Verification**: `verify_check.py` - Verify processing results
5. **Debugging**: Various fix scripts as needed

## Maintenance

If you need to modify the data structure or add new processing steps:

1. Review the existing scripts for reference
2. Create new scripts following the same patterns
3. Test thoroughly on a small subset of data
4. Document any changes in this README

## Warning

These scripts modify data files. Always:
- Create backups before running
- Test on a small subset first
- Verify results before processing the full dataset
