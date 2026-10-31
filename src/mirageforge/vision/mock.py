"""
Mock vision model backend for testing and demonstration.

Provides deterministic pseudo-predictions based on stimulus checksums.
Clearly marked as mock - not a real vision model.
"""

from typing import Any

import numpy as np
from PIL import Image

from mirageforge.utils.hashing import hash_bytes
from mirageforge.vision.base import VisionBackend


class MockVisionModel(VisionBackend):
    """
    Mock vision model for testing and demonstration.
    
    Generates deterministic pseudo-predictions based on stimulus properties.
    This is NOT a real vision model - it's a placeholder for testing the
    pipeline without requiring actual ML models.
    
    All outputs are clearly marked as MOCK.
    """
    
    def __init__(self, model_name: str = "MockVisionModel", version: str = "1.0.0"):
        """
        Initialize mock model.
        
        Args:
            model_name: Model name identifier
            version: Model version string
        """
        self._name = model_name
        self._version = version
    
    @property
    def name(self) -> str:
        """Get model name."""
        return self._name
    
    @property
    def version(self) -> str:
        """Get model version."""
        return self._version
    
    @property
    def is_mock(self) -> bool:
        """This is a mock backend."""
        return True
    
    def predict(self, image: Image.Image, task_spec: dict[str, Any]) -> dict[str, Any]:
        """
        Generate mock predictions based on image properties.
        
        Predictions are deterministic given the same image and task.
        Uses image hash to seed a random number generator for reproducibility.
        
        Args:
            image: PIL Image of the stimulus
            task_spec: Task specification with options
            
        Returns:
            Dictionary with mock prediction scores
        """
        # Convert image to bytes for hashing
        import io
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        # Use hash to seed RNG for deterministic predictions
        image_hash = hash_bytes(image_bytes)
        seed = int(image_hash[:8], 16)
        rng = np.random.default_rng(seed)
        
        # Get options from task spec
        options = task_spec.get("options", [])
        if not options:
            return {"error": "No options in task_spec", "is_mock": True}
        
        # Generate random scores that sum to 1.0
        raw_scores = rng.random(len(options))
        normalized_scores = raw_scores / raw_scores.sum()
        
        # Create prediction dictionary
        predictions = {}
        for i, option in enumerate(options):
            predictions[option] = float(normalized_scores[i])
        
        # Add metadata
        result = {
            "predictions": predictions,
            "is_mock": True,
            "model_name": self.name,
            "model_version": self.version,
            "note": "MOCK PREDICTIONS - Not from a real vision model",
        }
        
        return result
    
    def is_available(self) -> bool:
        """Mock model is always available."""
        return True
    
    def get_info(self) -> dict[str, Any]:
        """Get model information."""
        info = super().get_info()
        info.update({
            "description": "Mock vision model for testing and demonstration",
            "limitations": [
                "Not a real vision model",
                "Predictions are random but deterministic",
                "Should not be used for scientific conclusions",
            ],
            "use_case": "Testing pipeline, demonstrating interface",
        })
        return info
