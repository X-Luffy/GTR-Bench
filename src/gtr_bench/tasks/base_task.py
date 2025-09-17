"""
Base task class for GTR-Bench tasks.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseTask(ABC):
    """Base class for all GTR-Bench tasks."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the task.
        
        Args:
            config: Task configuration dictionary
        """
        self.config = config
        self.task_name = config.get('task_name', self.__class__.__name__)
        self.description = config.get('description', '')
        self.logger = logging.getLogger(f"{__name__}.{self.task_name}")
        
    @abstractmethod
    def load_data(self, data_path: str) -> List[Dict[str, Any]]:
        """
        Load task data from the specified path.
        
        Args:
            data_path: Path to the data directory
            
        Returns:
            List of data samples
        """
        pass
        
    @abstractmethod
    def evaluate_sample(self, sample: Dict[str, Any], model_output: str) -> Dict[str, float]:
        """
        Evaluate model output for a single sample.
        
        Args:
            sample: Input sample
            model_output: Model's output/prediction
            
        Returns:
            Dictionary of metric scores
        """
        pass
        
    @abstractmethod
    def get_metrics(self) -> List[str]:
        """
        Get list of metrics used by this task.
        
        Returns:
            List of metric names
        """
        pass
        
    def preprocess_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess a sample before evaluation.
        
        Args:
            sample: Raw sample data
            
        Returns:
            Preprocessed sample
        """
        return sample
        
    def format_prompt(self, sample: Dict[str, Any]) -> str:
        """
        Format the input prompt for the model.
        
        Args:
            sample: Input sample
            
        Returns:
            Formatted prompt string
        """
        return sample.get('question', '')
        
    def aggregate_metrics(self, results: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Aggregate metrics across multiple samples.
        
        Args:
            results: List of per-sample metric results
            
        Returns:
            Aggregated metrics
        """
        if not results:
            return {}
            
        aggregated = {}
        for metric in self.get_metrics():
            values = [result.get(metric, 0.0) for result in results]
            aggregated[metric] = sum(values) / len(values)
            
        return aggregated