"""
Unit tests for active search algorithms.
"""

from mirageforge.search.acquisition import (
    DiversityAcquisition,
    RandomAcquisition,
    UCBAcquisition,
)
from mirageforge.search.candidates import CandidateGenerator
from mirageforge.stimuli.dsl import StimulusFamily


class TestCandidateGenerator:
    """Tests for CandidateGenerator."""

    def test_candidate_generator_initialization(self):
        """Test CandidateGenerator initialization."""
        generator = CandidateGenerator(seed=42)
        assert generator.seed == 42

    def test_generate_random_candidates(self):
        """Test random candidate generation."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(count=20)

        assert len(candidates) == 20
        for spec in candidates:
            assert hasattr(spec, "family")
            assert hasattr(spec, "seed")
            assert hasattr(spec, "params")

    def test_generate_with_specific_families(self):
        """Test generation with specific families."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(
            count=10, families=[StimulusFamily.SIZE_CONTEXT, StimulusFamily.CONTRAST]
        )

        assert len(candidates) == 10
        families = {spec.family for spec in candidates}
        assert families.issubset({StimulusFamily.SIZE_CONTEXT, StimulusFamily.CONTRAST})

    def test_mutate_candidates(self):
        """Test candidate mutation."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(count=5)

        mutated = generator.mutate(candidates, mutation_rate=0.3, num_mutations=2)

        # Should generate some mutated candidates
        assert len(mutated) > 0
        for spec in mutated:
            assert hasattr(spec, "family")
            assert hasattr(spec, "seed")


class TestRandomAcquisition:
    """Tests for RandomAcquisition strategy."""

    def test_random_acquisition_initialization(self):
        """Test RandomAcquisition initialization."""
        acquisition = RandomAcquisition(seed=42)
        assert acquisition.rng is not None

    def test_random_acquisition_select(self):
        """Test random selection."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(count=20)

        acquisition = RandomAcquisition(seed=42)
        selected = acquisition.select(candidates, count=5)

        assert len(selected) == 5
        for spec in selected:
            assert spec in candidates


class TestUCBAcquisition:
    """Tests for UCBAcquisition strategy."""

    def test_ucb_acquisition_initialization(self):
        """Test UCBAcquisition initialization."""
        acquisition = UCBAcquisition(exploration_weight=1.5, seed=42)
        assert acquisition.exploration_weight == 1.5

    def test_ucb_acquisition_select(self):
        """Test UCB selection."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(count=20)

        acquisition = UCBAcquisition(seed=42)
        selected = acquisition.select(candidates, count=5)

        assert len(selected) == 5

    def test_ucb_with_scores(self):
        """Test UCB with provided scores."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(count=10)

        acquisition = UCBAcquisition(seed=42)
        scores = dict.fromkeys(range(10), 0.5)
        selected = acquisition.select(candidates, scores=scores, count=3)

        assert len(selected) == 3


class TestDiversityAcquisition:
    """Tests for DiversityAcquisition strategy."""

    def test_diversity_acquisition_initialization(self):
        """Test DiversityAcquisition initialization."""
        acquisition = DiversityAcquisition(num_bins=5, seed=42)
        assert acquisition.num_bins == 5

    def test_diversity_acquisition_select(self):
        """Test diversity-based selection."""
        generator = CandidateGenerator(seed=42)
        candidates = generator.generate_random(count=20)

        acquisition = DiversityAcquisition(seed=42)
        selected = acquisition.select(candidates, count=5)

        assert len(selected) == 5
