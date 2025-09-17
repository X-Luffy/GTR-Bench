"""
Dataset loaders and utilities for GTR-Bench.
"""

from .base_dataset import BaseDataset
from .gtr_dataset import GTRDataset
from .dataset_registry import DatasetRegistry

# Initialize the global dataset registry
dataset_registry = DatasetRegistry()

# Register default datasets
dataset_registry.register('gtr_dataset', GTRDataset)

__all__ = [
    'BaseDataset',
    'GTRDataset', 
    'DatasetRegistry',
    'dataset_registry'
]