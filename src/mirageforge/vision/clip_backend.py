"""
CLIP vision model backend (optional).

Provides real vision model predictions using OpenAI's CLIP.
Requires torch and transformers to be installed.
Gracefully degrades if dependencies are unavailable.
"""

import warnings
from typing import Any

from PIL import Image

from mirageforge.vision.base import VisionBackend, VisionBackendUnavailableError


class CLIPVisionBackend(VisionBackend):
    """
    CLIP vision model backend.

    Uses OpenAI's CLIP model to generate predictions based on
    image-text similarity. Requires torch and transformers.

    This is an optional backend. If dependencies are not available,
    the backend will report as unavailable and can be skipped.
    """

    def __init__(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
        device: str = "cpu",
    ):
        """
        Initialize CLIP backend.

        Args:
            model_name: Hugging Face model name
            device: Device to run on ("cpu" or "cuda")
        """
        self._model_name = model_name
        self._device = device
        self._model = None
        self._processor = None
        self._available = False

        # Try to load model
        self._try_load_model()

    def _try_load_model(self) -> None:
        """Attempt to load CLIP model and processor."""
        try:
            from transformers import CLIPModel, CLIPProcessor

            # Load model and processor
            self._processor = CLIPProcessor.from_pretrained(self._model_name)
            self._model = CLIPModel.from_pretrained(self._model_name)
            self._model = self._model.to(self._device)
            self._model.eval()

            self._available = True

        except ImportError as e:
            warnings.warn(
                f"CLIP backend dependencies not available: {e}. "
                "Install with: pip install torch transformers",
                UserWarning,
                stacklevel=2,
            )
            self._available = False
        except Exception as e:
            warnings.warn(
                f"Failed to load CLIP model: {e}",
                UserWarning,
                stacklevel=2,
            )
            self._available = False

    @property
    def name(self) -> str:
        """Get model name."""
        return f"CLIP-{self._model_name.split('/')[-1]}"

    @property
    def version(self) -> str:
        """Get model version."""
        return self._model_name

    @property
    def is_mock(self) -> bool:
        """This is a real vision model."""
        return False

    def predict(self, image: Image.Image, task_spec: dict[str, Any]) -> dict[str, Any]:
        """
        Generate CLIP predictions based on image-text similarity.

        Args:
            image: PIL Image of the stimulus
            task_spec: Task specification with options (as text prompts)

        Returns:
            Dictionary with CLIP prediction scores
        """
        if not self._available:
            raise VisionBackendUnavailableError(
                "CLIP backend is not available. Install torch and transformers."
            )

        import torch

        options = task_spec.get("options", [])
        if not options:
            return {"error": "No options in task_spec"}

        # Prepare inputs
        inputs = self._processor(
            text=options,
            images=image,
            return_tensors="pt",
            padding=True,
        )
        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        # Generate predictions
        with torch.no_grad():
            outputs = self._model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)[0].cpu().numpy()

        # Create prediction dictionary
        predictions = {}
        for i, option in enumerate(options):
            predictions[option] = float(probs[i])

        result = {
            "predictions": predictions,
            "is_mock": False,
            "model_name": self.name,
            "model_version": self.version,
            "note": "CLIP model predictions based on image-text similarity",
        }

        return result

    def is_available(self) -> bool:
        """Check if CLIP backend is available."""
        return self._available

    def get_info(self) -> dict[str, Any]:
        """Get model information."""
        info = super().get_info()
        info.update({
            "description": "OpenAI CLIP model for vision-language predictions",
            "model_name": self._model_name,
            "device": self._device,
            "limitations": [
                "Requires torch and transformers",
                "May be slow on CPU",
                "Not specifically trained on illusions",
                "Image-text similarity may not match human perception",
            ],
            "use_case": "Comparing with human responses, identifying divergence",
        })
        return info
