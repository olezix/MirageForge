"""
Generator for size context stimuli (Ebbinghaus-like).

Generates parameterized stimuli that test size perception in context.
"""

from typing import Optional

import numpy as np

from mirageforge.stimuli.dsl import (
    SafetyFlags,
    SizeContextParams,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)


def generate_size_context_stimuli(
    count: int,
    base_seed: int,
    target_size_range: tuple[float, float] = (30.0, 80.0),
    context_size_range: tuple[float, float] = (40.0, 150.0),
) -> list[StimulusSpec]:
    """
    Generate random size context stimuli.
    
    Args:
        count: Number of stimuli to generate
        base_seed: Base random seed
        target_size_range: Range for target circle size
        context_size_range: Range for context circle size
        
    Returns:
        List of StimulusSpec objects
    """
    rng = np.random.default_rng(base_seed)
    stimuli: list[StimulusSpec] = []
    
    for i in range(count):
        seed = base_seed + i + 1
        
        # Generate parameters
        target_size = float(rng.uniform(*target_size_range))
        context_size = float(rng.uniform(*context_size_range))
        
        # Ensure context doesn't overlap with target
        min_distance = (target_size + context_size) / 2 + 20
        context_distance = float(rng.uniform(min_distance, min(min_distance + 100, 350)))
        
        num_context = int(rng.integers(4, 9))
        
        # Random colors
        colors = ["#808080", "#A0A0A0", "#606060", "#707070"]
        context_color = rng.choice(colors)
        
        params = SizeContextParams(
            target_size=target_size,
            context_size=context_size,
            context_distance=context_distance,
            num_context=num_context,
            context_color=context_color,
            target_color="#000000",
            background_color="#FFFFFF",
        )
        
        # Task: Which circle is larger? (2AFC)
        # In reality both are same size, but context makes them appear different
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["Left circle is larger", "Right circle is larger"],
            correct_answer=None,  # No correct answer in illusion
            question="Which circle appears larger?",
        )
        
        safety = SafetyFlags(
            has_flashing=False,
            has_fast_motion=False,
            has_high_contrast=False,
        )
        
        spec = StimulusSpec(
            family=StimulusFamily.SIZE_CONTEXT,
            params=params,
            task=task,
            seed=seed,
            safety=safety,
        )
        
        stimuli.append(spec)
    
    return stimuli
