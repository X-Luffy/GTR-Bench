"""
Evaluation metrics for GTR-Bench.
"""

from .accuracy import accuracy_score
from .spatial_metrics import spatial_accuracy, reasoning_consistency
from .f1_score import f1_score
from .metric_registry import MetricRegistry

# Initialize the global metric registry
metric_registry = MetricRegistry()

# Register default metrics
metric_registry.register('accuracy', accuracy_score)
metric_registry.register('spatial_accuracy', spatial_accuracy)
metric_registry.register('reasoning_consistency', reasoning_consistency)
metric_registry.register('f1_score', f1_score)

__all__ = [
    'accuracy_score',
    'spatial_accuracy', 
    'reasoning_consistency',
    'f1_score',
    'MetricRegistry',
    'metric_registry'
]