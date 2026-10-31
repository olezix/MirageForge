"""
Acquisition strategies for active search.

Implements different strategies for selecting candidates to evaluate:
- Random: uniform random selection
- UCB: Upper Confidence Bound for exploration-exploitation tradeoff
"""

from abc import ABC, abstractmethod

import numpy as np

from mirageforge.stimuli.dsl import StimulusSpec


class AcquisitionStrategy(ABC):
    """Abstract base class for acquisition strategies."""

    @abstractmethod
    def select(
        self,
        candidates: list[StimulusSpec],
        scores: dict[int, float] | None = None,
        count: int = 10,
    ) -> list[StimulusSpec]:
        """
        Select candidates for evaluation.

        Args:
            candidates: Pool of candidates to select from
            scores: Optional dictionary mapping candidate index to score
            count: Number of candidates to select

        Returns:
            List of selected candidates
        """
        pass


class RandomAcquisition(AcquisitionStrategy):
    """
    Random acquisition strategy.

    Selects candidates uniformly at random. Simple baseline strategy.
    """

    def __init__(self, seed: int = 42):
        """
        Initialize random acquisition.

        Args:
            seed: Random seed
        """
        self.rng = np.random.default_rng(seed)

    def select(
        self,
        candidates: list[StimulusSpec],
        scores: dict[int, float] | None = None,
        count: int = 10,
    ) -> list[StimulusSpec]:
        """Select candidates randomly."""
        if count >= len(candidates):
            return candidates

        indices = self.rng.choice(len(candidates), size=count, replace=False)
        return [candidates[i] for i in indices]


class UCBAcquisition(AcquisitionStrategy):
    """
    Upper Confidence Bound (UCB) acquisition strategy.

    Balances exploration (uncertainty) and exploitation (high scores).
    Selects candidates with high predicted divergence or high uncertainty.
    """

    def __init__(self, exploration_weight: float = 1.0, seed: int = 42):
        """
        Initialize UCB acquisition.

        Args:
            exploration_weight: Weight for exploration term (higher = more exploration)
            seed: Random seed
        """
        self.exploration_weight = exploration_weight
        self.rng = np.random.default_rng(seed)
        self.visit_counts: dict[int, int] = {}
        self.total_visits = 0

    def select(
        self,
        candidates: list[StimulusSpec],
        scores: dict[int, float] | None = None,
        count: int = 10,
    ) -> list[StimulusSpec]:
        """
        Select candidates using UCB.

        UCB = mean_score + exploration_weight * sqrt(ln(N) / n_i)
        where N = total visits, n_i = visits to candidate i
        """
        if scores is None:
            scores = {}

        # Initialize scores with small random values for unseen candidates
        for i in range(len(candidates)):
            if i not in scores:
                scores[i] = float(self.rng.uniform(0.4, 0.6))

        # Calculate UCB values
        ucb_values = {}
        for i in range(len(candidates)):
            mean_score = scores.get(i, 0.5)
            visits = self.visit_counts.get(i, 0)

            # UCB formula
            if visits == 0:
                # Never visited: high exploration bonus
                ucb_values[i] = mean_score + self.exploration_weight * 10.0
            else:
                exploration_bonus = self.exploration_weight * np.sqrt(
                    np.log(max(1, self.total_visits)) / visits
                )
                ucb_values[i] = mean_score + exploration_bonus

        # Select top candidates by UCB value
        sorted_indices = sorted(ucb_values.keys(), key=lambda i: ucb_values[i], reverse=True)
        selected_indices = sorted_indices[:count]

        # Update visit counts
        for i in selected_indices:
            self.visit_counts[i] = self.visit_counts.get(i, 0) + 1
            self.total_visits += 1

        return [candidates[i] for i in selected_indices]

    def update_score(self, index: int, score: float) -> None:
        """
        Update the score for a candidate.

        Args:
            index: Candidate index
            score: New score
        """
        # In a full implementation, this would update running averages
        # For simplicity, we just track visits
        pass


class DiversityAcquisition(AcquisitionStrategy):
    """
    Diversity-based acquisition strategy.

    Selects candidates that maximize diversity in parameter space.
    Uses parameter binning to ensure coverage of different regions.
    """

    def __init__(self, num_bins: int = 5, seed: int = 42):
        """
        Initialize diversity acquisition.

        Args:
            num_bins: Number of bins per parameter dimension
            seed: Random seed
        """
        self.num_bins = num_bins
        self.rng = np.random.default_rng(seed)
        self.covered_bins: set[tuple[int, ...]] = set()

    def select(
        self,
        candidates: list[StimulusSpec],
        scores: dict[int, float] | None = None,
        count: int = 10,
    ) -> list[StimulusSpec]:
        """Select candidates to maximize parameter diversity."""
        # Bin candidates by their parameters
        candidate_bins: dict[tuple[int, ...], list[int]] = {}

        for i, candidate in enumerate(candidates):
            bin_key = self._get_bin_key(candidate)
            if bin_key not in candidate_bins:
                candidate_bins[bin_key] = []
            candidate_bins[bin_key].append(i)

        # Select from uncovered bins first
        selected_indices = []

        # Prioritize uncovered bins
        uncovered_bins = [b for b in candidate_bins.keys() if b not in self.covered_bins]
        self.rng.shuffle(uncovered_bins)

        for bin_key in uncovered_bins:
            if len(selected_indices) >= count:
                break
            # Select one candidate from this bin
            if candidate_bins[bin_key]:
                idx = self.rng.choice(candidate_bins[bin_key])
                selected_indices.append(idx)
                self.covered_bins.add(bin_key)

        # Fill remaining slots randomly
        remaining = count - len(selected_indices)
        if remaining > 0:
            available = [i for i in range(len(candidates)) if i not in selected_indices]
            if available:
                extra = self.rng.choice(available, size=min(remaining, len(available)), replace=False)
                selected_indices.extend(extra.tolist())

        return [candidates[i] for i in selected_indices[:count]]

    def _get_bin_key(self, candidate: StimulusSpec) -> tuple[int, ...]:
        """Get bin key for a candidate based on its parameters."""
        params = candidate.get_param_dict()

        # Select key parameters for binning
        bin_values = []

        # Bin family
        bin_values.append(int(candidate.family.value.encode()[0] % self.num_bins))

        # Bin seed
        bin_values.append(int(candidate.seed % self.num_bins))

        # Bin first numeric parameter
        for _key, value in params.items():
            if isinstance(value, (int, float)):
                # Normalize to [0, 1] and bin
                normalized = (value % 100) / 100.0
                bin_idx = int(normalized * self.num_bins)
                bin_values.append(min(bin_idx, self.num_bins - 1))
                break

        return tuple(bin_values)
