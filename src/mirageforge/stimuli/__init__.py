"""
Stimulus generation and rendering.

Provides DSL for parameterized visual stimuli and deterministic
rendering to PNG images with SHA256 checksums.
"""

from mirageforge.stimuli.dsl import (
    ContrastParams,
    CrowdingParams,
    GratingParams,
    LineContextParams,
    SafetyFlags,
    SizeContextParams,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)
from mirageforge.stimuli.renderer import StimulusRenderer

__all__ = [
    "StimulusSpec",
    "StimulusFamily",
    "TaskSpec",
    "TaskType",
    "SafetyFlags",
    "SizeContextParams",
    "LineContextParams",
    "ContrastParams",
    "CrowdingParams",
    "GratingParams",
    "StimulusRenderer",
]
