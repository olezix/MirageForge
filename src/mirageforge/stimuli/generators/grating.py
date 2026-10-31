"""
Generator for grating detection stimuli.

Generates parameterized stimuli that test contrast sensitivity and detection thresholds.
"""

import numpy as np

from mirageforge.stimuli.dsl import (
    GratingParams,
    SafetyFlags,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)


def generate_grating_stimuli(
    count: int,
    base_seed: int,
    contrast_range: tuple[float, float] = (0.05, 0.9),
    frequency_range: tuple[float, float] = (0.5, 12.0),
) -> list[StimulusSpec]:
    """
    Generate random grating stimuli.
    
    Args:
        count: Number of stimuli to generate
        base_seed: Base random seed
        contrast_range: Range for Michelson contrast
        frequency_range: Range for spatial frequency
        
    Returns:
        List of StimulusSpec objects
    """
    rng = np.random.default_rng(base_seed)
    stimuli: list[StimulusSpec] = []
    
    envelopes = ["gaussian", "circular", "square"]
    
    for i in range(count):
        seed = base_seed + i + 1
        
        # Generate parameters
        spatial_frequency = float(rng.uniform(*frequency_range))
        contrast = float(rng.uniform(*contrast_range))
        orientation = float(rng.uniform(0.0, 180.0))
        phase = float(rng.uniform(0.0, 360.0))
        aperture_size = float(rng.uniform(200.0, 600.0))
        envelope = rng.choice(envelopes)
        
        params = GratingParams(
            spatial_frequency=spatial_frequency,
            contrast=contrast,
            orientation=orientation,
            phase=phase,
            aperture_size=aperture_size,
            envelope=envelope,
        )
        
        # Task: Is there a pattern? (yes/no)
        task = TaskSpec(
            task_type=TaskType.YES_NO,
            options=["Yes, I see a pattern", "No, it's uniform"],
            correct_answer=None,
            question="Do you see a striped pattern?",
        )
        
        # Check for high contrast + high frequency
        has_high_contrast = spatial_frequency > 8.0 and contrast > 0.7
        
        safety = SafetyFlags(
            has_flashing=False,
            has_fast_motion=False,
            has_high_contrast=has_high_contrast,
            warning_text="Fine pattern - may cause discomfort" if has_high_contrast else None,
        )
        
        spec = StimulusSpec(
            family=StimulusFamily.GRATING,
            params=params,
            task=task,
            seed=seed,
            safety=safety,
        )
        
        stimuli.append(spec)
    
    return stimuli
