"""
Stimulus generators for all families.

Provides functions to generate random stimulus specifications within
safe parameter ranges for each stimulus family.
"""

from mirageforge.stimuli.generators.contrast import generate_contrast_stimuli
from mirageforge.stimuli.generators.crowding import generate_crowding_stimuli
from mirageforge.stimuli.generators.grating import generate_grating_stimuli
from mirageforge.stimuli.generators.line_context import generate_line_context_stimuli
from mirageforge.stimuli.generators.size_context import generate_size_context_stimuli

__all__ = [
    "generate_size_context_stimuli",
    "generate_line_context_stimuli",
    "generate_contrast_stimuli",
    "generate_crowding_stimuli",
    "generate_grating_stimuli",
]
