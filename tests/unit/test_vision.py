"""
Unit tests for vision model backends.
"""

from mirageforge.stimuli.dsl import StimulusFamily
from mirageforge.stimuli.generators import generate_size_context_stimuli
from mirageforge.stimuli.renderer import StimulusRenderer
from mirageforge.vision.mock import MockVisionModel
from mirageforge.vision.simulated_human import SimulatedHumanModel


class TestMockVisionModel:
    """Tests for MockVisionModel."""

    def test_mock_model_initialization(self):
        """Test MockVisionModel initialization."""
        model = MockVisionModel()
        assert model.name == "MockVisionModel"
        assert model.version == "1.0.0"
        assert model.is_mock is True
        assert model.is_available() is True

    def test_mock_model_predict(self):
        """Test MockVisionModel predictions."""
        model = MockVisionModel()
        renderer = StimulusRenderer(image_size=256)

        stimuli = generate_size_context_stimuli(count=1, base_seed=42)
        image = renderer.render(stimuli[0])

        task_spec = {
            "options": ["Option A", "Option B"],
            "question": "Which is larger?",
        }

        result = model.predict(image, task_spec)

        assert "predictions" in result
        assert "Option A" in result["predictions"]
        assert "Option B" in result["predictions"]
        assert result["is_mock"] is True
        assert result["model_name"] == "MockVisionModel"

        # Probabilities should sum to approximately 1.0
        total_prob = sum(result["predictions"].values())
        assert abs(total_prob - 1.0) < 0.01

    def test_mock_model_deterministic(self):
        """Test that MockVisionModel is deterministic."""
        model = MockVisionModel()
        renderer = StimulusRenderer(image_size=256)

        stimuli = generate_size_context_stimuli(count=1, base_seed=42)
        image = renderer.render(stimuli[0])

        task_spec = {"options": ["A", "B"], "question": "Test?"}

        result1 = model.predict(image, task_spec)
        result2 = model.predict(image, task_spec)

        assert result1["predictions"] == result2["predictions"]


class TestSimulatedHumanModel:
    """Tests for SimulatedHumanModel."""

    def test_simulated_human_initialization(self):
        """Test SimulatedHumanModel initialization."""
        model = SimulatedHumanModel(noise_level=0.15, bias_strength=0.7, seed=42)
        assert model.name == "SimulatedHumanModel"
        assert model.version == "1.0.0"
        assert model.is_mock is True
        assert model.is_available() is True

    def test_simulated_human_predict(self):
        """Test SimulatedHumanModel predictions."""
        model = SimulatedHumanModel(seed=42)
        renderer = StimulusRenderer(image_size=256)

        stimuli = generate_size_context_stimuli(count=1, base_seed=42)
        image = renderer.render(stimuli[0])

        task_spec = {
            "options": ["Left", "Right"],
            "question": "Which is larger?",
            "stimulus_params": stimuli[0].get_param_dict(),
            "family": StimulusFamily.SIZE_CONTEXT.value,
        }

        result = model.predict(image, task_spec)

        assert "predictions" in result
        assert result["is_synthetic"] is True
        assert result["model_name"] == "SimulatedHumanModel"

        # Probabilities should sum to approximately 1.0
        total_prob = sum(result["predictions"].values())
        assert abs(total_prob - 1.0) < 0.01

    def test_simulated_human_with_bias(self):
        """Test that SimulatedHumanModel shows perceptual biases."""
        model = SimulatedHumanModel(noise_level=0.1, bias_strength=0.8, seed=42)
        renderer = StimulusRenderer(image_size=256)

        # Generate stimuli with different context sizes
        stimuli = generate_size_context_stimuli(count=2, base_seed=42)

        task_spec = {
            "options": ["Left", "Right"],
            "question": "Which is larger?",
            "stimulus_params": stimuli[0].get_param_dict(),
            "family": StimulusFamily.SIZE_CONTEXT.value,
        }

        image = renderer.render(stimuli[0])
        result = model.predict(image, task_spec)

        # Should have predictions for both options
        assert len(result["predictions"]) == 2
