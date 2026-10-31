"""
Vision model backends for comparing with human responses.

Provides interfaces and implementations for vision models including
mock models, simulated human models, and optional CLIP integration.
"""

from mirageforge.vision.base import VisionBackend, VisionBackendError
from mirageforge.vision.clip_backend import CLIPVisionBackend
from mirageforge.vision.mock import MockVisionModel
from mirageforge.vision.simulated_human import SimulatedHumanModel

__all__ = [
    "VisionBackend",
    "VisionBackendError",
    "MockVisionModel",
    "SimulatedHumanModel",
    "CLIPVisionBackend",
]
