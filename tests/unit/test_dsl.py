"""
Unit tests for stimulus DSL and generators.
"""

from mirageforge.stimuli.dsl import (
    StimulusFamily,
    StimulusSpec,
    TaskType,
)
from mirageforge.stimuli.generators import (
    generate_contrast_stimuli,
    generate_crowding_stimuli,
    generate_grating_stimuli,
    generate_line_context_stimuli,
    generate_size_context_stimuli,
)


class TestStimulusGenerators:
    """Tests for stimulus generators."""

    def test_generate_size_context_stimuli(self):
        """Test size context stimulus generation."""
        stimuli = generate_size_context_stimuli(count=5, base_seed=42)

        assert len(stimuli) == 5
        for stim in stimuli:
            assert isinstance(stim, StimulusSpec)
            assert stim.family == StimulusFamily.SIZE_CONTEXT
            assert stim.seed >= 0
            assert stim.task.task_type == TaskType.TWO_AFC

    def test_generate_line_context_stimuli(self):
        """Test line context stimulus generation."""
        stimuli = generate_line_context_stimuli(count=5, base_seed=42)

        assert len(stimuli) == 5
        for stim in stimuli:
            assert isinstance(stim, StimulusSpec)
            assert stim.family == StimulusFamily.LINE_CONTEXT

    def test_generate_contrast_stimuli(self):
        """Test contrast stimulus generation."""
        stimuli = generate_contrast_stimuli(count=5, base_seed=42)

        assert len(stimuli) == 5
        for stim in stimuli:
            assert isinstance(stim, StimulusSpec)
            assert stim.family == StimulusFamily.CONTRAST

    def test_generate_crowding_stimuli(self):
        """Test crowding stimulus generation."""
        stimuli = generate_crowding_stimuli(count=5, base_seed=42)

        assert len(stimuli) == 5
        for stim in stimuli:
            assert isinstance(stim, StimulusSpec)
            assert stim.family == StimulusFamily.CROWDING

    def test_generate_grating_stimuli(self):
        """Test grating stimulus generation."""
        stimuli = generate_grating_stimuli(count=5, base_seed=42)

        assert len(stimuli) == 5
        for stim in stimuli:
            assert isinstance(stim, StimulusSpec)
            assert stim.family == StimulusFamily.GRATING

    def test_deterministic_generation(self):
        """Test that generation is deterministic with same seed."""
        stimuli1 = generate_size_context_stimuli(count=3, base_seed=100)
        stimuli2 = generate_size_context_stimuli(count=3, base_seed=100)

        assert len(stimuli1) == len(stimuli2)
        for s1, s2 in zip(stimuli1, stimuli2, strict=False):
            assert s1.seed == s2.seed
            assert s1.family == s2.family

    def test_different_seeds_produce_different_stimuli(self):
        """Test that different seeds produce different stimuli."""
        stimuli1 = generate_size_context_stimuli(count=3, base_seed=100)
        stimuli2 = generate_size_context_stimuli(count=3, base_seed=200)

        # Seeds should be different
        seeds1 = {s.seed for s in stimuli1}
        seeds2 = {s.seed for s in stimuli2}
        assert seeds1 != seeds2
