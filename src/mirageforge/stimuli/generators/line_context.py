"""
Generator for line context stimuli (Müller-Lyer/Poggendorff-like).

Generates parameterized stimuli that test line length perception in context.
"""

import numpy as np

from mirageforge.stimuli.dsl import (
    LineContextParams,
    SafetyFlags,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)


def generate_line_context_stimuli(
    count: int,
    base_seed: int,
    line_length_range: tuple[float, float] = (100.0, 300.0),
) -> list[StimulusSpec]:
    """
    Generate random line context stimuli.

    Args:
        count: Number of stimuli to generate
        base_seed: Base random seed
        line_length_range: Range for main line length

    Returns:
        List of StimulusSpec objects
    """
    rng = np.random.default_rng(base_seed)
    stimuli: list[StimulusSpec] = []

    for i in range(count):
        seed = base_seed + i + 1

        # Generate parameters
        line_length = float(rng.uniform(*line_length_range))
        line_width = float(rng.uniform(2.0, 8.0))
        arrow_angle = float(rng.uniform(20.0, 70.0))
        arrow_length = float(rng.uniform(30.0, 100.0))
        arrow_type = rng.choice(["inward", "outward", "neutral"])

        params = LineContextParams(
            line_length=line_length,
            line_width=line_width,
            arrow_angle=arrow_angle,
            arrow_length=arrow_length,
            arrow_type=arrow_type,
            line_color="#000000",
            background_color="#FFFFFF",
        )

        # Task: Which line is longer? (2AFC)
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["Top line is longer", "Bottom line is longer"],
            correct_answer=None,
            question="Which line appears longer?",
        )

        safety = SafetyFlags(
            has_flashing=False,
            has_fast_motion=False,
            has_high_contrast=False,
        )

        spec = StimulusSpec(
            family=StimulusFamily.LINE_CONTEXT,
            params=params,
            task=task,
            seed=seed,
            safety=safety,
        )

        stimuli.append(spec)

    return stimuli
