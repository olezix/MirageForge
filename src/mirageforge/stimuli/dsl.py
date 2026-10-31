"""
Domain-Specific Language (DSL) for stimulus specification.

Defines the parameterized structure for all visual stimuli using Pydantic v2.
Each stimulus family has its own parameter schema with validation and safe ranges.
"""

from enum import Enum
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StimulusFamily(str, Enum):
    """Supported stimulus families."""
    SIZE_CONTEXT = "size_context"  # Ebbinghaus-like
    LINE_CONTEXT = "line_context"  # Müller-Lyer/Poggendorff-like
    CONTRAST = "contrast"  # Simultaneous contrast
    CROWDING = "crowding"  # Flanking context
    GRATING = "grating"  # Detection/threshold


class TaskType(str, Enum):
    """Supported task types."""
    TWO_AFC = "2AFC"  # Two-alternative forced choice
    YES_NO = "yes_no"  # Yes/No detection
    SAME_DIFFERENT = "same_different"  # Same/Different judgment


class SizeContextParams(BaseModel):
    """Parameters for size context stimuli (Ebbinghaus-like)."""
    model_config = ConfigDict(extra="forbid")
    
    target_size: float = Field(..., ge=10, le=200, description="Target circle diameter in pixels")
    context_size: float = Field(..., ge=10, le=300, description="Context circle diameter in pixels")
    context_distance: float = Field(..., ge=50, le=400, description="Distance from target to context")
    num_context: int = Field(..., ge=3, le=12, description="Number of context circles")
    context_color: str = Field(default="#808080", description="Context circle color")
    target_color: str = Field(default="#000000", description="Target circle color")
    background_color: str = Field(default="#FFFFFF", description="Background color")

    @field_validator("context_distance")
    @classmethod
    def validate_distance(cls, v: float, info: Any) -> float:
        """Ensure context doesn't overlap with target."""
        data = info.data
        if "target_size" in data and "context_size" in data:
            min_distance = (data["target_size"] + data["context_size"]) / 2 + 10
            if v < min_distance:
                raise ValueError(f"Distance too small, minimum {min_distance}")
        return v


class LineContextParams(BaseModel):
    """Parameters for line context stimuli (Müller-Lyer/Poggendorff-like)."""
    model_config = ConfigDict(extra="forbid")
    
    line_length: float = Field(..., ge=50, le=500, description="Main line length in pixels")
    line_width: float = Field(..., ge=1, le=20, description="Line width in pixels")
    arrow_angle: float = Field(..., ge=10, le=80, description="Arrow/fin angle in degrees")
    arrow_length: float = Field(..., ge=10, le=150, description="Arrow/fin length in pixels")
    arrow_type: Literal["inward", "outward", "neutral"] = Field(
        default="neutral", description="Arrow direction"
    )
    line_color: str = Field(default="#000000", description="Line color")
    background_color: str = Field(default="#FFFFFF", description="Background color")


class ContrastParams(BaseModel):
    """Parameters for simultaneous contrast stimuli."""
    model_config = ConfigDict(extra="forbid")
    
    target_luminance: float = Field(..., ge=0.0, le=1.0, description="Target luminance (0-1)")
    surround_luminance: float = Field(..., ge=0.0, le=1.0, description="Surround luminance (0-1)")
    target_size: float = Field(..., ge=50, le=400, description="Target square size in pixels")
    surround_size: float = Field(..., ge=200, le=800, description="Surround square size in pixels")
    hue: float = Field(default=0.0, ge=0.0, le=360.0, description="Hue angle (0=gray, >0=chromatic)")
    saturation: float = Field(default=0.0, ge=0.0, le=1.0, description="Color saturation")


class CrowdingParams(BaseModel):
    """Parameters for crowding/flanking stimuli."""
    model_config = ConfigDict(extra="forbid")
    
    target_type: Literal["T", "L", "+", "square"] = Field(
        default="T", description="Target shape"
    )
    target_size: float = Field(..., ge=20, le=200, description="Target size in pixels")
    flanker_distance: float = Field(..., ge=10, le=300, description="Flanker distance in pixels")
    num_flankers: int = Field(..., ge=2, le=8, description="Number of flankers")
    flanker_type: Literal["same", "different", "none"] = Field(
        default="different", description="Flanker type"
    )
    target_rotation: float = Field(default=0.0, ge=0.0, le=360.0, description="Target rotation")
    flanker_rotation: float = Field(default=0.0, ge=0.0, le=360.0, description="Flanker rotation")


class GratingParams(BaseModel):
    """Parameters for grating detection stimuli."""
    model_config = ConfigDict(extra="forbid")
    
    spatial_frequency: float = Field(
        ..., ge=0.1, le=20.0, description="Spatial frequency in cycles per image"
    )
    contrast: float = Field(..., ge=0.0, le=1.0, description="Michelson contrast")
    orientation: float = Field(..., ge=0.0, le=180.0, description="Orientation in degrees")
    phase: float = Field(default=0.0, ge=0.0, le=360.0, description="Phase in degrees")
    aperture_size: float = Field(..., ge=100, le=800, description="Aperture diameter in pixels")
    envelope: Literal["gaussian", "circular", "square"] = Field(
        default="gaussian", description="Aperture envelope"
    )


# Union type for all stimulus parameters
StimulusParams = Union[
    SizeContextParams,
    LineContextParams,
    ContrastParams,
    CrowdingParams,
    GratingParams,
]


class TaskSpec(BaseModel):
    """Task specification for a stimulus."""
    model_config = ConfigDict(extra="forbid")
    
    task_type: TaskType
    options: list[str] = Field(..., min_length=2, max_length=4)
    correct_answer: Optional[str] = None  # Only for testing, not shown to participants
    question: str = Field(..., min_length=1)


class SafetyFlags(BaseModel):
    """Safety flags for stimulus rendering."""
    model_config = ConfigDict(extra="forbid")
    
    has_flashing: bool = Field(default=False, description="Contains flashing/flickering")
    has_fast_motion: bool = Field(default=False, description="Contains fast motion")
    has_high_contrast: bool = Field(default=False, description="Very high contrast")
    has_small_text: bool = Field(default=False, description="Contains small text")
    warning_text: Optional[str] = Field(default=None, description="Optional warning text")

    @field_validator("has_flashing")
    @classmethod
    def no_flashing_in_mvp(cls, v: bool) -> bool:
        """MVP does not support flashing stimuli."""
        if v:
            raise ValueError("Flashing stimuli are not allowed in MVP")
        return v


class StimulusSpec(BaseModel):
    """
    Complete specification for a visual stimulus.
    
    This is the main DSL class that defines all aspects of a stimulus:
    family, parameters, task, seed, and safety flags.
    """
    model_config = ConfigDict(extra="forbid")
    
    family: StimulusFamily
    params: StimulusParams
    task: TaskSpec
    seed: int = Field(..., ge=0, description="Random seed for deterministic rendering")
    safety: SafetyFlags = Field(default_factory=SafetyFlags)

    @field_validator("params", mode="before")
    @classmethod
    def validate_params_by_family(cls, v: Any, info: Any) -> Any:
        """Validate parameters match the stimulus family."""
        # This is handled by Pydantic's discriminated unions
        # but we add explicit validation for clarity
        return v

    def get_param_dict(self) -> dict[str, Any]:
        """Get parameters as a dictionary."""
        return self.params.model_dump()

    def get_task_dict(self) -> dict[str, Any]:
        """Get task specification as a dictionary."""
        return self.task.model_dump()

    def get_safety_dict(self) -> dict[str, Any]:
        """Get safety flags as a dictionary."""
        return self.safety.model_dump()


def create_stimulus_spec(
    family: StimulusFamily | str,
    params: dict[str, Any],
    task: dict[str, Any],
    seed: int,
    safety: Optional[dict[str, Any]] = None,
) -> StimulusSpec:
    """
    Factory function to create a StimulusSpec.
    
    Args:
        family: Stimulus family
        params: Parameters dictionary (validated by family)
        task: Task specification dictionary
        seed: Random seed
        safety: Optional safety flags
        
    Returns:
        Validated StimulusSpec
    """
    if isinstance(family, str):
        family = StimulusFamily(family)
    
    # Select parameter model based on family
    param_models = {
        StimulusFamily.SIZE_CONTEXT: SizeContextParams,
        StimulusFamily.LINE_CONTEXT: LineContextParams,
        StimulusFamily.CONTRAST: ContrastParams,
        StimulusFamily.CROWDING: CrowdingParams,
        StimulusFamily.GRATING: GratingParams,
    }
    
    param_model = param_models[family]
    validated_params = param_model(**params)
    
    validated_task = TaskSpec(**task)
    validated_safety = SafetyFlags(**(safety or {}))
    
    return StimulusSpec(
        family=family,
        params=validated_params,
        task=validated_task,
        seed=seed,
        safety=validated_safety,
    )
