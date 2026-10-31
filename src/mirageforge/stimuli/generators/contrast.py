"""
Generator for simultaneous contrast stimuli.

Generates parameterized stimuli that test brightness and color perception.
"""

import numpy as np

from mirageforge.stimuli.dsl import (
    ContrastParams,
    SafetyFlags,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)


def generate_contrast_stimuli(
    count: int,
    base_seed: int,
    luminance_range: tuple[float, float] = (0.2, 0.8),
) -> list[StimulusSpec]:
    """
    Generate random contrast stimuli.

    Args:
        count: Number of stimuli to generate
        base_seed: Base random seed
        luminance_range: Range for luminance values

    Returns:
        List of StimulusSpec objects
    """
    rng = np.random.default_rng(base_seed)
    stimuli: list[StimulusSpec] = []

    for i in range(count):
        seed = base_seed + i + 1

        # Generate parameters
        target_luminance = float(rng.uniform(*luminance_range))
        surround_luminance = float(rng.uniform(*luminance_range))

        # Ensure some difference
        if abs(target_luminance - surround_luminance) < 0.1:
            surround_luminance = (surround_luminance + 0.3) % 1.0

        target_size = float(rng.uniform(100.0, 250.0))
        surround_size = float(rng.uniform(400.0, 700.0))

        # Mostly grayscale, occasionally chromatic
        if rng.random() < 0.2:
            hue = float(rng.uniform(0.0, 360.0))
            saturation = float(rng.uniform(0.3, 0.7))
        else:
            hue = 0.0
            saturation = 0.0

        params = ContrastParams(
            target_luminance=target_luminance,
            surround_luminance=surround_luminance,
            target_size=target_size,
            surround_size=surround_size,
            hue=hue,
            saturation=saturation,
        )

        # Task: Which patch is brighter? (2AFC)
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["Left patch is brighter", "Right patch is brighter"],
            correct_answer=None,
            question="Which patch appears brighter?",
        )

        # Check for high contrast
        lum_diff = abs(target_luminance - surround_luminance)
        has_high_contrast = lum_diff > 0.7

        safety = SafetyFlags(
            has_flashing=False,
            has_fast_motion=False,
            has_high_contrast=has_high_contrast,
            warning_text="High contrast stimulus" if has_high_contrast else None,
        )

        spec = StimulusSpec(
            family=StimulusFamily.CONTRAST,
            params=params,
            task=task,
            seed=seed,
            safety=safety,
        )

        stimuli.append(spec)

    return stimuli
