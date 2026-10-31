"""
Base interface for vision model backends.

Defines the contract that all vision backends must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from PIL import Image


class VisionBackend(ABC):
    """
    Abstract base class for vision model backends.
    
    All vision backends must implement this interface to be used
    in the MirageForge platform for comparing with human responses.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the model name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Get the model version."""
        pass
    
    @property
    @abstractmethod
    def is_mock(self) -> bool:
        """Check if this is a mock/synthetic backend."""
        pass
    
    @abstractmethod
    def predict(self, image: Image.Image, task_spec: dict[str, Any]) -> dict[str, Any]:
        """
        Generate predictions for a stimulus.
        
        Args:
            image: PIL Image of the stimulus
            task_spec: Task specification (question, options, etc.)
            
        Returns:
            Dictionary with prediction scores/probabilities for each option
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the backend is available and ready to use.
        
        Returns:
            True if backend is ready, False otherwise
        """
        pass
    
    def get_info(self) -> dict[str, Any]:
        """
        Get model information for documentation.
        
        Returns:
            Dictionary with model metadata
        """
        return {
            "name": self.name,
            "version": self.version,
            "is_mock": self.is_mock,
            "is_available": self.is_available(),
        }


class VisionBackendError(Exception):
    """Exception raised when a vision backend encounters an error."""
    pass


class VisionBackendUnavailableError(VisionBackendError):
    """Exception raised when a vision backend is not available."""
    pass
