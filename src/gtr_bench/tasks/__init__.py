"""
Task definitions and implementations for GTR-Bench.
"""

from .base_task import BaseTask
from .spatial_reasoning import SpatialReasoningTask
from .spatial_understanding import SpatialUnderstandingTask
from .spatial_navigation import SpatialNavigationTask
from .object_relations import ObjectRelationsTask

__all__ = [
    'BaseTask',
    'SpatialReasoningTask', 
    'SpatialUnderstandingTask',
    'SpatialNavigationTask',
    'ObjectRelationsTask'
]