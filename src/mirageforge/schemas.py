"""
Pydantic schemas for data validation and serialization.

These schemas provide runtime validation and type safety for all
data structures used in the application.
"""

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudyBase(BaseModel):
    """Base schema for Study."""
    title: str = Field(..., min_length=1, max_length=255)
    version: str = Field(default="1.0.0", max_length=50)
    consent_text: str = Field(..., min_length=10)
    active: bool = Field(default=True)
    config: dict[str, Any] = Field(default_factory=dict)


class StudyCreate(StudyBase):
    """Schema for creating a Study."""
    pass


class StudyUpdate(BaseModel):
    """Schema for updating a Study."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    version: Optional[str] = Field(None, max_length=50)
    consent_text: Optional[str] = Field(None, min_length=10)
    active: Optional[bool] = None
    config: Optional[dict[str, Any]] = None


class StudyResponse(StudyBase):
    """Schema for Study response."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StimulusBase(BaseModel):
    """Base schema for Stimulus."""
    family: str = Field(..., min_length=1, max_length=100)
    params: dict[str, Any] = Field(...)
    seed: int = Field(..., ge=0)
    task_spec: dict[str, Any] = Field(...)
    intended_effect: Optional[str] = None
    safety_flags: dict[str, Any] = Field(default_factory=dict)


class StimulusCreate(StimulusBase):
    """Schema for creating a Stimulus."""
    study_id: Optional[int] = None


class StimulusResponse(StimulusBase):
    """Schema for Stimulus response."""
    id: int
    study_id: Optional[int]
    image_path: str
    sha256: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionCreate(BaseModel):
    """Schema for creating a Session."""
    study_id: int
    consent_version: str = Field(..., max_length=50)


class SessionResponse(BaseModel):
    """Schema for Session response."""
    id: str
    study_id: int
    consent_version: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class TrialBase(BaseModel):
    """Base schema for Trial."""
    stimulus_id: int
    task_type: Literal["2AFC", "yes_no", "same_different"]
    option_order: dict[str, Any]


class TrialCreate(TrialBase):
    """Schema for creating a Trial."""
    session_id: str


class TrialResponse(TrialBase):
    """Schema for Trial response."""
    id: int
    session_id: str
    presented_at: datetime
    stimulus: StimulusResponse

    model_config = ConfigDict(from_attributes=True)


class ResponseCreate(BaseModel):
    """Schema for creating a Response."""
    trial_id: int
    choice: str = Field(..., min_length=1, max_length=100)
    reaction_time_ms: int = Field(..., ge=0, le=300000)  # Max 5 minutes
    confidence: Optional[int] = Field(None, ge=1, le=10)

    @field_validator("reaction_time_ms")
    @classmethod
    def validate_reaction_time(cls, v: int) -> int:
        """Validate reaction time is reasonable."""
        if v < 50:
            raise ValueError("Reaction time too short (<50ms)")
        if v > 300000:
            raise ValueError("Reaction time too long (>5min)")
        return v


class ResponseResponse(BaseModel):
    """Schema for Response response."""
    id: int
    trial_id: int
    choice: str
    reaction_time_ms: int
    confidence: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ModelRunBase(BaseModel):
    """Base schema for ModelRun."""
    model_name: str = Field(..., min_length=1, max_length=100)
    model_version: str = Field(..., max_length=50)
    stimulus_id: int
    probe: dict[str, Any]
    scores: dict[str, Any]


class ModelRunCreate(ModelRunBase):
    """Schema for creating a ModelRun."""
    pass


class ModelRunResponse(ModelRunBase):
    """Schema for ModelRun response."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditEventCreate(BaseModel):
    """Schema for creating an AuditEvent."""
    event_type: str = Field(..., min_length=1, max_length=100)
    metadata_json: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata_json")
    @classmethod
    def validate_no_pii(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate that metadata does not contain PII."""
        pii_fields = {"ip", "ip_address", "email", "name", "user_agent", "address", "phone"}
        for key in v.keys():
            if key.lower() in pii_fields:
                raise ValueError(f"PII field '{key}' not allowed in audit metadata")
        return v


class AuditEventResponse(BaseModel):
    """Schema for AuditEvent response."""
    id: int
    event_type: str
    metadata_json: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    version: str
    timestamp: datetime


class ExperimentConfig(BaseModel):
    """Configuration for an experiment session."""
    study_id: int
    trials_count: int = Field(default=12, ge=1, le=100)
    randomize_order: bool = Field(default=True)
    balanced_options: bool = Field(default=True)


class StatsSummary(BaseModel):
    """Summary statistics for a study."""
    study_id: int
    total_sessions: int
    completed_sessions: int
    total_trials: int
    total_responses: int
    is_synthetic: bool
    created_at: datetime


class DivergenceMetric(BaseModel):
    """Divergence metric between human and model responses."""
    stimulus_id: int
    family: str
    absolute_difference: float = Field(..., ge=0.0, le=1.0)
    jensen_shannon_divergence: float = Field(..., ge=0.0, le=1.0)
    p_value: Optional[float] = None
    significant: bool = False
    sample_size: int
