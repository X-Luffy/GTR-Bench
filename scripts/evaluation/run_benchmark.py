#!/usr/bin/env python3
"""
Script to run GTR-Bench evaluation.
"""

import argparse
import logging
import yaml
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Run GTR-Bench evaluation")
    parser.add_argument(
        "--config", 
        type=str, 
        default="configs/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--model-config",
        type=str,
        help="Path to model configuration file"
    )
    parser.add_argument(
        "--task", 
        type=str,
        help="Specific task to evaluate (if not specified, runs all tasks)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for results"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    logger.info(f"Loading configuration from {args.config}")
    config = load_config(args.config)
    
    # Override config with command line arguments
    if args.model_config:
        config['model']['config_path'] = args.model_config
    if args.task:
        config['tasks'] = [args.task]
    if args.output_dir:
        config['evaluation']['output_dir'] = args.output_dir
    
    logger.info("Starting GTR-Bench evaluation...")
    logger.info(f"Tasks to evaluate: {config['tasks']}")
    
    # TODO: Implement evaluation pipeline
    # This is a template - actual evaluation logic would go here
    
    logger.info("Evaluation completed successfully!")

if __name__ == "__main__":
    main()