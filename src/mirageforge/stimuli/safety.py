"""
Safety checks for visual stimuli.

Ensures all stimuli meet safety requirements:
- No flashing or flickering
- No fast motion or animation
- Appropriate contrast levels
- No photosensitive triggers
"""

from typing import Any

from mirageforge.stimuli.dsl import SafetyFlags, StimulusSpec


class SafetyValidationError(Exception):
    """Raised when a stimulus fails safety validation."""
    pass


def validate_stimulus_safety(spec: StimulusSpec) -> tuple[bool, list[str]]:
    """
    Validate that a stimulus meets all safety requirements.
    
    Args:
        spec: Stimulus specification
        
    Returns:
        Tuple of (is_safe, list of warnings)
        
    Raises:
        SafetyValidationError: If stimulus violates hard safety constraints
    """
    warnings: list[str] = []
    
    # Hard constraint: No flashing in MVP
    if spec.safety.has_flashing:
        raise SafetyValidationError(
            "Flashing stimuli are not allowed in MVP. "
            "This feature may be added in future versions with proper safety protocols."
        )
    
    # Hard constraint: No fast motion in MVP
    if spec.safety.has_fast_motion:
        raise SafetyValidationError(
            "Fast motion stimuli are not allowed in MVP. "
            "Only static images are supported."
        )
    
    # Soft warnings for high contrast
    if spec.safety.has_high_contrast:
        warnings.append(
            "This stimulus has very high contrast which may cause discomfort for some participants."
        )
    
    # Check family-specific safety
    family_warnings = _validate_family_safety(spec)
    warnings.extend(family_warnings)
    
    is_safe = True  # Hard constraints passed
    return is_safe, warnings


def _validate_family_safety(spec: StimulusSpec) -> list[str]:
    """Validate family-specific safety concerns."""
    warnings: list[str] = []
    
    from mirageforge.stimuli.dsl import (
        ContrastParams,
        CrowdingParams,
        GratingParams,
        LineContextParams,
        SizeContextParams,
        StimulusFamily,
    )
    
    # Check contrast stimuli
    if spec.family == StimulusFamily.CONTRAST and isinstance(spec.params, ContrastParams):
        # Warn if luminance difference is extreme
        lum_diff = abs(spec.params.target_luminance - spec.params.surround_luminance)
        if lum_diff > 0.9:
            warnings.append(
                "Extreme luminance difference may cause visual discomfort or afterimages."
            )
    
    # Check grating stimuli
    if spec.family == StimulusFamily.GRATING and isinstance(spec.params, GratingParams):
        # Warn for high spatial frequencies with high contrast
        if spec.params.spatial_frequency > 10.0 and spec.params.contrast > 0.8:
            warnings.append(
                "High spatial frequency with high contrast may cause visual discomfort."
            )
    
    # Check crowding stimuli
    if spec.family == StimulusFamily.CROWDING and isinstance(spec.params, CrowdingParams):
        # Warn for very small targets
        if spec.params.target_size < 30:
            warnings.append(
                "Very small target size may cause eye strain."
            )
    
    # Check size context stimuli
    if spec.family == StimulusFamily.SIZE_CONTEXT and isinstance(spec.params, SizeContextParams):
        # Warn for extreme size ratios
        size_ratio = spec.params.context_size / spec.params.target_size
        if size_ratio > 5.0 or size_ratio < 0.2:
            warnings.append(
                "Extreme size ratio between target and context may cause discomfort."
            )
    
    # Check line context stimuli
    if spec.family == StimulusFamily.LINE_CONTEXT and isinstance(spec.params, LineContextParams):
        # Warn for very thin lines
        if spec.params.line_width < 2:
            warnings.append(
                "Very thin lines may be difficult to see and cause eye strain."
            )
    
    return warnings


def generate_safety_flags(spec: StimulusSpec) -> SafetyFlags:
    """
    Automatically generate safety flags based on stimulus parameters.
    
    Args:
        spec: Stimulus specification
        
    Returns:
        SafetyFlags with appropriate warnings
    """
    from mirageforge.stimuli.dsl import (
        ContrastParams,
        GratingParams,
        StimulusFamily,
    )
    
    has_high_contrast = False
    warning_text = None
    
    # Check for high contrast
    if spec.family == StimulusFamily.CONTRAST and isinstance(spec.params, ContrastParams):
        lum_diff = abs(spec.params.target_luminance - spec.params.surround_luminance)
        if lum_diff > 0.8:
            has_high_contrast = True
            warning_text = "This stimulus has high contrast. Look away if you experience discomfort."
    
    # Check for high-frequency gratings
    if spec.family == StimulusFamily.GRATING and isinstance(spec.params, GratingParams):
        if spec.params.spatial_frequency > 8.0 and spec.params.contrast > 0.7:
            has_high_contrast = True
            warning_text = "This stimulus contains fine patterns. Look away if you experience discomfort."
    
    return SafetyFlags(
        has_flashing=False,  # MVP constraint
        has_fast_motion=False,  # MVP constraint
        has_high_contrast=has_high_contrast,
        has_small_text=False,  # No text in stimuli
        warning_text=warning_text,
    )


def get_safety_disclaimer() -> str:
    """
    Get standard safety disclaimer for experiments.
    
    Returns:
        Disclaimer text
    """
    return (
        "This experiment displays visual patterns on your screen. "
        "Some patterns may cause mild visual discomfort. "
        "If you experience any discomfort, eye strain, or headache, "
        "please stop immediately and look away from the screen. "
        "You may stop the experiment at any time without penalty. "
        "This experiment does not use flashing lights or fast-moving images."
    )


def get_photosensitivity_warning() -> str:
    """
    Get photosensitivity warning (for future use if flashing is added).
    
    Returns:
        Warning text
    """
    return (
        "WARNING: This experiment may contain visual patterns. "
        "If you have photosensitive epilepsy or are sensitive to visual patterns, "
        "please consult with a healthcare provider before participating. "
        "Stop immediately if you experience any discomfort."
    )
