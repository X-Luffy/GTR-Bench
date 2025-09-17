#!/usr/bin/env python3
"""
Simple evaluation example for GTR-Bench.
"""

import sys
from pathlib import Path
import yaml
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def main():
    """Run a simple evaluation example."""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("GTR-Bench Simple Evaluation Example")
    logger.info("====================================")
    
    # Load configuration
    config_path = Path(__file__).parent.parent.parent / "configs" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Loaded configuration: {config_path}")
    logger.info(f"Tasks to evaluate: {config['tasks']}")
    
    # Example evaluation steps
    logger.info("Step 1: Initialize model...")
    # TODO: Initialize model based on config
    
    logger.info("Step 2: Load datasets...")
    # TODO: Load datasets for each task
    
    logger.info("Step 3: Run evaluation...")
    # TODO: Run evaluation pipeline
    
    logger.info("Step 4: Compute metrics...")
    # TODO: Compute and aggregate metrics
    
    logger.info("Step 5: Save results...")
    # TODO: Save results to output directory
    
    logger.info("Evaluation completed!")
    logger.info("This is a template - implement actual evaluation logic in the GTR-Bench library")

if __name__ == "__main__":
    main()