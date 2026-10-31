"""
Candidate stimulus generation and mutation.

Generates diverse candidate stimuli for active search and optimization.
"""


import numpy as np

from mirageforge.stimuli.dsl import StimulusFamily, StimulusSpec
from mirageforge.stimuli.generators import (
    generate_contrast_stimuli,
    generate_crowding_stimuli,
    generate_grating_stimuli,
    generate_line_context_stimuli,
    generate_size_context_stimuli,
)


class CandidateGenerator:
    """
    Generates candidate stimuli for active search.

    Supports random generation and mutation of existing candidates
    to explore the stimulus space efficiently.
    """

    def __init__(self, seed: int = 42):
        """
        Initialize candidate generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def generate_random(
        self,
        count: int,
        families: list[StimulusFamily] | None = None,
    ) -> list[StimulusSpec]:
        """
        Generate random candidate stimuli.

        Args:
            count: Number of candidates to generate
            families: List of families to sample from (default: all)

        Returns:
            List of candidate StimulusSpec objects
        """
        if families is None:
            families = list(StimulusFamily)

        candidates: list[StimulusSpec] = []

        # Distribute candidates across families
        per_family = max(1, count // len(families))
        remainder = count - per_family * len(families)

        base_seed = self.seed

        for i, family in enumerate(families):
            family_count = per_family + (1 if i < remainder else 0)

            if family == StimulusFamily.SIZE_CONTEXT:
                family_candidates = generate_size_context_stimuli(
                    count=family_count,
                    base_seed=base_seed,
                )
            elif family == StimulusFamily.LINE_CONTEXT:
                family_candidates = generate_line_context_stimuli(
                    count=family_count,
                    base_seed=base_seed,
                )
            elif family == StimulusFamily.CONTRAST:
                family_candidates = generate_contrast_stimuli(
                    count=family_count,
                    base_seed=base_seed,
                )
            elif family == StimulusFamily.CROWDING:
                family_candidates = generate_crowding_stimuli(
                    count=family_count,
                    base_seed=base_seed,
                )
            elif family == StimulusFamily.GRATING:
                family_candidates = generate_grating_stimuli(
                    count=family_count,
                    base_seed=base_seed,
                )
            else:
                continue

            candidates.extend(family_candidates)
            base_seed += family_count + 1000

        return candidates[:count]

    def mutate(
        self,
        candidates: list[StimulusSpec],
        mutation_rate: float = 0.3,
        num_mutations: int = 10,
    ) -> list[StimulusSpec]:
        """
        Mutate existing candidates to explore nearby parameter space.

        Args:
            candidates: List of candidates to mutate
            mutation_rate: Probability of mutating each parameter
            num_mutations: Number of mutations per candidate

        Returns:
            List of mutated candidates
        """
        mutated: list[StimulusSpec] = []

        for candidate in candidates:
            for _ in range(num_mutations):
                mutated_candidate = self._mutate_single(candidate, mutation_rate)
                if mutated_candidate:
                    mutated.append(mutated_candidate)

        return mutated

    def _mutate_single(
        self,
        candidate: StimulusSpec,
        mutation_rate: float,
    ) -> StimulusSpec | None:
        """Mutate a single candidate."""
        try:
            # Get current parameters
            params_dict = candidate.get_param_dict()

            # Mutate parameters
            mutated_params = {}
            for key, value in params_dict.items():
                if self.rng.random() < mutation_rate:
                    mutated_params[key] = self._mutate_parameter(key, value, candidate.family)
                else:
                    mutated_params[key] = value

            # Create new spec with mutated parameters
            new_seed = candidate.seed + int(self.rng.integers(1, 10000))

            # Import here to avoid circular dependency
            from mirageforge.stimuli.dsl import create_stimulus_spec

            new_spec = create_stimulus_spec(
                family=candidate.family,
                params=mutated_params,
                task=candidate.get_task_dict(),
                seed=new_seed,
                safety=candidate.get_safety_dict(),
            )

            return new_spec

        except Exception:
            # Mutation failed (e.g., validation error), skip
            return None

    def _mutate_parameter(self, key: str, value: any, family: StimulusFamily) -> any:
        """Mutate a single parameter value."""
        if isinstance(value, (int, float)):
            # Numeric parameter: add Gaussian noise
            if isinstance(value, int):
                noise = int(self.rng.normal(0, max(1, abs(value) * 0.1)))
                return max(1, value + noise)
            else:
                noise = self.rng.normal(0, max(0.01, abs(value) * 0.1))
                return value + noise
        elif isinstance(value, str):
            # String parameter: keep as is (could implement color mutations)
            return value
        else:
            # Other types: keep as is
            return value


def generate_candidates(
    count: int,
    seed: int = 42,
    families: list[StimulusFamily] | None = None,
) -> list[StimulusSpec]:
    """
    Convenience function to generate random candidates.

    Args:
        count: Number of candidates
        seed: Random seed
        families: Optional list of families

    Returns:
        List of candidate stimuli
    """
    generator = CandidateGenerator(seed=seed)
    return generator.generate_random(count=count, families=families)


def mutate_candidates(
    candidates: list[StimulusSpec],
    seed: int = 42,
    mutation_rate: float = 0.3,
    num_mutations: int = 5,
) -> list[StimulusSpec]:
    """
    Convenience function to mutate candidates.

    Args:
        candidates: Candidates to mutate
        seed: Random seed
        mutation_rate: Mutation probability
        num_mutations: Mutations per candidate

    Returns:
        List of mutated candidates
    """
    generator = CandidateGenerator(seed=seed)
    return generator.mutate(
        candidates=candidates,
        mutation_rate=mutation_rate,
        num_mutations=num_mutations,
    )
