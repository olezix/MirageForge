"""
Generator for crowding/flanking stimuli.

Generates parameterized stimuli that test object recognition in cluttered scenes.
"""

import numpy as np

from mirageforge.stimuli.dsl import (
    CrowdingParams,
    SafetyFlags,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)


def generate_crowding_stimuli(
    count: int,
    base_seed: int,
    target_size_range: tuple[float, float] = (40.0, 120.0),
) -> list[StimulusSpec]:
    """
    Generate random crowding stimuli.

    Args:
        count: Number of stimuli to generate
        base_seed: Base random seed
        target_size_range: Range for target size

    Returns:
        List of StimulusSpec objects
    """
    rng = np.random.default_rng(base_seed)
    stimuli: list[StimulusSpec] = []

    target_types = ["T", "L", "+", "square"]
    flanker_types = ["same", "different", "none"]

    for i in range(count):
        seed = base_seed + i + 1

        # Generate parameters
        target_type = rng.choice(target_types)
        target_size = float(rng.uniform(*target_size_range))
        # Ensure flanker_distance is within valid range (10-300)
        min_distance = max(10.0, target_size * 1.2)
        max_distance = min(300.0, target_size * 3.0)
        if min_distance > max_distance:
            max_distance = min_distance + 10.0
        flanker_distance = float(rng.uniform(min_distance, max_distance))
        num_flankers = int(rng.integers(2, 7))
        flanker_type = rng.choice(flanker_types)

        target_rotation = float(rng.uniform(0.0, 360.0))
        flanker_rotation = float(rng.uniform(0.0, 360.0))

        params = CrowdingParams(
            target_type=target_type,
            target_size=target_size,
            flanker_distance=flanker_distance,
            num_flankers=num_flankers,
            flanker_type=flanker_type,
            target_rotation=target_rotation,
            flanker_rotation=flanker_rotation,
        )

        # Task: What is the central shape? (multiple choice)
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["T shape", "L shape", "+ shape", "Square"],
            correct_answer=None,
            question="What is the shape in the center?",
        )

        safety = SafetyFlags(
            has_flashing=False,
            has_fast_motion=False,
            has_high_contrast=False,
        )

        spec = StimulusSpec(
            family=StimulusFamily.CROWDING,
            params=params,
            task=task,
            seed=seed,
            safety=safety,
        )

        stimuli.append(spec)

    return stimuli
