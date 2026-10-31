"""
SQLAlchemy database models for MirageForge.

All models follow privacy-by-design principles:
- No IP addresses, user agents, or personally identifiable information
- Only anonymous UUID session tokens
- Timestamps are stored for analysis but not linked to individuals
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Study(Base):
    """
    Study configuration for an experiment.

    A study defines the parameters, consent text, and configuration for a research experiment.
    Multiple sessions can belong to the same study.
    """
    __tablename__ = "studies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    consent_text: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="study")
    stimuli: Mapped[list["Stimulus"]] = relationship("Stimulus", back_populates="study")

    def __repr__(self) -> str:
        return f"<Study(id={self.id}, title='{self.title}', version='{self.version}')>"


class Stimulus(Base):
    """
    Visual stimulus with parameterized configuration.

    Each stimulus is uniquely identified by its family, parameters, and seed.
    The SHA256 checksum ensures reproducibility and integrity.
    """
    __tablename__ = "stimuli"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    study_id: Mapped[int] = mapped_column(Integer, ForeignKey("studies.id"), nullable=True)
    family: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    params: Mapped[dict] = mapped_column(JSON, nullable=False)
    seed: Mapped[int] = mapped_column(Integer, nullable=False)
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    task_spec: Mapped[dict] = mapped_column(JSON, nullable=False)
    intended_effect: Mapped[str | None] = mapped_column(Text, nullable=True)
    safety_flags: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    study: Mapped[Optional["Study"]] = relationship("Study", back_populates="stimuli")
    trials: Mapped[list["Trial"]] = relationship("Trial", back_populates="stimulus")
    model_runs: Mapped[list["ModelRun"]] = relationship("ModelRun", back_populates="stimulus")

    def __repr__(self) -> str:
        return f"<Stimulus(id={self.id}, family='{self.family}', seed={self.seed})>"


class Session(Base):
    """
    Anonymous experiment session.

    Each session represents one participant's interaction with the experiment.
    Sessions are identified by random UUIDs with no personally identifiable information.
    """
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID
    study_id: Mapped[int] = mapped_column(Integer, ForeignKey("studies.id"), nullable=False)
    consent_version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="in_progress", nullable=False
    )  # in_progress, completed, abandoned
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    study: Mapped["Study"] = relationship("Study", back_populates="sessions")
    trials: Mapped[list["Trial"]] = relationship("Trial", back_populates="session")

    def __repr__(self) -> str:
        return f"<Session(id='{self.id}', status='{self.status}')>"


class Trial(Base):
    """
    Single trial within a session.

    A trial presents one stimulus to the participant and records their response.
    """
    __tablename__ = "trials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("sessions.id"), nullable=False)
    stimulus_id: Mapped[int] = mapped_column(Integer, ForeignKey("stimuli.id"), nullable=False)
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 2AFC, yes_no, same_different
    option_order: Mapped[dict] = mapped_column(JSON, nullable=False)  # Randomized option order
    presented_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="trials")
    stimulus: Mapped["Stimulus"] = relationship("Stimulus", back_populates="trials")
    response: Mapped[Optional["Response"]] = relationship("Response", back_populates="trial", uselist=False)

    def __repr__(self) -> str:
        return f"<Trial(id={self.id}, task_type='{self.task_type}')>"


class Response(Base):
    """
    Participant's response to a trial.

    Records the choice, reaction time, and optional confidence rating.
    No personally identifiable information is stored.
    """
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trial_id: Mapped[int] = mapped_column(Integer, ForeignKey("trials.id"), nullable=False, unique=True)
    choice: Mapped[str] = mapped_column(String(100), nullable=False)
    reaction_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Optional confidence rating
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    trial: Mapped["Trial"] = relationship("Trial", back_populates="response")

    def __repr__(self) -> str:
        return f"<Response(id={self.id}, choice='{self.choice}', rt={self.reaction_time_ms}ms)>"


class ModelRun(Base):
    """
    Vision model prediction for a stimulus.

    Records the model's scores/predictions for a given stimulus.
    Used to compare with human responses and identify divergence.
    """
    __tablename__ = "model_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    stimulus_id: Mapped[int] = mapped_column(Integer, ForeignKey("stimuli.id"), nullable=False)
    probe: Mapped[dict] = mapped_column(JSON, nullable=False)  # Input probe/question
    scores: Mapped[dict] = mapped_column(JSON, nullable=False)  # Model predictions
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    stimulus: Mapped["Stimulus"] = relationship("Stimulus", back_populates="model_runs")

    def __repr__(self) -> str:
        return f"<ModelRun(id={self.id}, model='{self.model_name}', stimulus_id={self.stimulus_id})>"


class AuditEvent(Base):
    """
    Audit log for system events.

    Records important system events without storing personally identifiable information.
    Used for debugging and compliance.
    """
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)  # Non-PII metadata only
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<AuditEvent(id={self.id}, type='{self.event_type}')>"
