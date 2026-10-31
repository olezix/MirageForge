"""
Simulated human model for synthetic experiments.

Generates synthetic human-like responses based on parameterized psychometric
functions. Clearly marked as SYNTHETIC - not real human data.
"""

from typing import Any

import numpy as np
from PIL import Image

from mirageforge.stimuli.dsl import (
    StimulusFamily,
)
from mirageforge.vision.base import VisionBackend


class SimulatedHumanModel(VisionBackend):
    """
    Simulated human observer model.

    Generates synthetic responses that mimic human perceptual biases
    and variability. Uses parameterized psychometric functions based on
    known illusion effects from the literature.

    IMPORTANT: This is a SYNTHETIC model, not real human data.
    All outputs are clearly marked as SYNTHETIC.
    """

    def __init__(
        self,
        noise_level: float = 0.15,
        bias_strength: float = 0.7,
        seed: int = 42,
    ):
        """
        Initialize simulated human model.

        Args:
            noise_level: Amount of response variability (0-1)
            bias_strength: Strength of perceptual biases (0-1)
            seed: Random seed for reproducibility
        """
        self._name = "SimulatedHumanModel"
        self._version = "1.0.0"
        self.noise_level = noise_level
        self.bias_strength = bias_strength
        self.rng = np.random.default_rng(seed)

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
        """This is a synthetic backend."""
        return True

    def predict(self, image: Image.Image, task_spec: dict[str, Any]) -> dict[str, Any]:
        """
        Generate synthetic human-like predictions.

        Simulates known perceptual biases for different stimulus families.

        Args:
            image: PIL Image of the stimulus
            task_spec: Task specification with options and stimulus params

        Returns:
            Dictionary with synthetic prediction scores
        """
        options = task_spec.get("options", [])
        if not options:
            return {"error": "No options in task_spec", "is_synthetic": True}

        # Get stimulus parameters if available
        stimulus_params = task_spec.get("stimulus_params", {})
        family = task_spec.get("family", "unknown")

        # Generate biased predictions based on stimulus family
        if family == StimulusFamily.SIZE_CONTEXT.value:
            probabilities = self._simulate_size_context(stimulus_params, len(options))
        elif family == StimulusFamily.LINE_CONTEXT.value:
            probabilities = self._simulate_line_context(stimulus_params, len(options))
        elif family == StimulusFamily.CONTRAST.value:
            probabilities = self._simulate_contrast(stimulus_params, len(options))
        elif family == StimulusFamily.CROWDING.value:
            probabilities = self._simulate_crowding(stimulus_params, len(options))
        elif family == StimulusFamily.GRATING.value:
            probabilities = self._simulate_grating(stimulus_params, len(options))
        else:
            # Default: near-random with slight bias
            probabilities = self._generate_biased_random(len(options))

        # Create prediction dictionary
        predictions = {}
        for i, option in enumerate(options):
            predictions[option] = float(probabilities[i])

        result = {
            "predictions": predictions,
            "is_synthetic": True,
            "model_name": self.name,
            "model_version": self.version,
            "note": "SYNTHETIC HUMAN RESPONSES - Not from real participants",
            "noise_level": self.noise_level,
            "bias_strength": self.bias_strength,
        }

        return result

    def _simulate_size_context(self, params: dict[str, Any], num_options: int) -> np.ndarray:
        """Simulate size context illusion (Ebbinghaus-like)."""
        # Humans tend to perceive target as smaller when surrounded by large context
        context_size = params.get("context_size", 50.0)
        target_size = params.get("target_size", 50.0)

        size_ratio = context_size / target_size

        # Bias towards first option if context is large
        if size_ratio > 1.5:
            bias = 0.5 + self.bias_strength * 0.3
        elif size_ratio < 0.7:
            bias = 0.5 - self.bias_strength * 0.3
        else:
            bias = 0.5

        return self._generate_biased_random(num_options, bias)

    def _simulate_line_context(self, params: dict[str, Any], num_options: int) -> np.ndarray:
        """Simulate line context illusion (Müller-Lyer-like)."""
        arrow_type = params.get("arrow_type", "neutral")

        # Inward arrows make line appear shorter, outward makes it appear longer
        if arrow_type == "inward":
            bias = 0.5 - self.bias_strength * 0.25
        elif arrow_type == "outward":
            bias = 0.5 + self.bias_strength * 0.25
        else:
            bias = 0.5

        return self._generate_biased_random(num_options, bias)

    def _simulate_contrast(self, params: dict[str, Any], num_options: int) -> np.ndarray:
        """Simulate simultaneous contrast."""
        target_lum = params.get("target_luminance", 0.5)
        surround_lum = params.get("surround_luminance", 0.5)

        # Target appears brighter when surround is darker (and vice versa)
        lum_diff = surround_lum - target_lum
        bias = 0.5 + self.bias_strength * lum_diff * 0.3

        return self._generate_biased_random(num_options, bias)

    def _simulate_crowding(self, params: dict[str, Any], num_options: int) -> np.ndarray:
        """Simulate crowding effect."""
        flanker_type = params.get("flanker_type", "none")
        flanker_distance = params.get("flanker_distance", 100.0)
        target_size = params.get("target_size", 60.0)

        # Crowding is stronger when flankers are close and similar
        crowding_strength = 0.0
        if flanker_type == "same":
            crowding_strength = 0.3
        elif flanker_type == "different":
            crowding_strength = 0.15

        # Distance effect
        distance_ratio = flanker_distance / target_size
        if distance_ratio < 2.0:
            crowding_strength *= 1.5

        # Reduce accuracy with crowding
        bias = 0.5 + self.bias_strength * crowding_strength * 0.2

        return self._generate_biased_random(num_options, bias)

    def _simulate_grating(self, params: dict[str, Any], num_options: int) -> np.ndarray:
        """Simulate grating detection."""
        contrast = params.get("contrast", 0.5)
        frequency = params.get("spatial_frequency", 5.0)

        # Detection probability follows contrast sensitivity function
        # Peak sensitivity around 3-5 cycles/degree
        optimal_freq = 4.0
        freq_factor = np.exp(-((frequency - optimal_freq) ** 2) / (2 * 2.0**2))

        # Contrast threshold effect
        detection_prob = 1.0 / (1.0 + np.exp(-10 * (contrast - 0.1)))

        # Combine factors
        overall_prob = detection_prob * freq_factor
        bias = 0.5 + self.bias_strength * (overall_prob - 0.5) * 0.5

        return self._generate_biased_random(num_options, bias)

    def _generate_biased_random(self, num_options: int, bias: float = 0.5) -> np.ndarray:
        """
        Generate biased random probabilities.

        Args:
            num_options: Number of options
            bias: Bias towards first option (0-1, 0.5 = unbiased)

        Returns:
            Array of probabilities summing to 1.0
        """
        if num_options == 1:
            return np.array([1.0])

        # Generate base probabilities with bias
        probs = np.zeros(num_options)
        probs[0] = bias

        # Distribute remaining probability among other options
        remaining = 1.0 - bias
        for i in range(1, num_options):
            probs[i] = remaining / (num_options - 1)

        # Add noise
        noise = self.rng.normal(0, self.noise_level, num_options)
        probs = probs + noise

        # Normalize to sum to 1.0 and ensure all positive
        probs = np.maximum(probs, 0.01)
        probs = probs / probs.sum()

        return probs

    def is_available(self) -> bool:
        """Simulated model is always available."""
        return True

    def get_info(self) -> dict[str, Any]:
        """Get model information."""
        info = super().get_info()
        info.update({
            "description": "Simulated human observer with parameterized psychometric functions",
            "limitations": [
                "SYNTHETIC responses, not from real participants",
                "Based on simplified models of known illusions",
                "Does not capture full complexity of human perception",
                "Should not be used for scientific conclusions without real validation",
            ],
            "assumptions": [
                f"Noise level: {self.noise_level}",
                f"Bias strength: {self.bias_strength}",
                "Biases based on literature on classical illusions",
            ],
            "use_case": "Testing pipeline, demonstrating platform, synthetic validation",
        })
        return info
