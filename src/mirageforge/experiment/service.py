"""
Experiment service for managing sessions and trials.

Provides core functionality for running experiments with participants.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from mirageforge.models import Response, Session, Stimulus, Study, Trial
from mirageforge.schemas import (
    ExperimentConfig,
    ResponseCreate,
    SessionCreate,
    SessionResponse,
    TrialResponse,
)


class ExperimentService:
    """
    Service for managing experiment sessions and trials.
    
    Handles session creation, trial presentation, response recording,
    and session completion.
    """
    
    def __init__(self, db: DBSession):
        """
        Initialize experiment service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def create_session(self, session_data: SessionCreate) -> SessionResponse:
        """
        Create a new experiment session.
        
        Args:
            session_data: Session creation data
            
        Returns:
            Created session
        """
        # Generate UUID for session
        session_id = str(uuid.uuid4())
        
        # Create session
        session = Session(
            id=session_id,
            study_id=session_data.study_id,
            consent_version=session_data.consent_version,
            status="in_progress",
            created_at=datetime.utcnow(),
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return SessionResponse.model_validate(session)
    
    def get_next_trial(
        self,
        session_id: str,
        config: ExperimentConfig,
    ) -> Optional[TrialResponse]:
        """
        Get the next trial for a session.
        
        Args:
            session_id: Session ID
            config: Experiment configuration
            
        Returns:
            Next trial or None if session is complete
        """
        # Get session
        session = self.db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session.status != "in_progress":
            return None
        
        # Count completed trials
        completed_count = (
            self.db.query(Trial)
            .filter(Trial.session_id == session_id, Trial.response != None)
            .count()
        )
        
        if completed_count >= config.trials_count:
            # Session complete
            return None
        
        # Get stimuli for this study
        stimuli = (
            self.db.query(Stimulus)
            .filter(Stimulus.study_id == session.study_id)
            .all()
        )
        
        if not stimuli:
            raise ValueError(f"No stimuli found for study {session.study_id}")
        
        # Get already presented stimuli
        presented_ids = {
            t.stimulus_id
            for t in self.db.query(Trial).filter(Trial.session_id == session_id).all()
        }
        
        # Select next stimulus
        available = [s for s in stimuli if s.id not in presented_ids]
        if not available:
            # All stimuli presented, allow repeats
            available = stimuli
        
        # Randomize if configured
        if config.randomize_order:
            import random
            selected_stimulus = random.choice(available)
        else:
            selected_stimulus = available[0]
        
        # Create trial
        import random
        
        # Randomize option order if configured
        option_order = {}
        if config.balanced_options:
            options = selected_stimulus.task_spec.get("options", [])
            shuffled = options.copy()
            random.shuffle(shuffled)
            option_order = {opt: i for i, opt in enumerate(shuffled)}
        else:
            options = selected_stimulus.task_spec.get("options", [])
            option_order = {opt: i for i, opt in enumerate(options)}
        
        trial = Trial(
            session_id=session_id,
            stimulus_id=selected_stimulus.id,
            task_type=selected_stimulus.task_spec.get("task_type", "2AFC"),
            option_order=option_order,
            presented_at=datetime.utcnow(),
        )
        
        self.db.add(trial)
        self.db.commit()
        self.db.refresh(trial)
        
        # Build response with stimulus
        trial_dict = {
            "id": trial.id,
            "session_id": trial.session_id,
            "stimulus_id": trial.stimulus_id,
            "task_type": trial.task_type,
            "option_order": trial.option_order,
            "presented_at": trial.presented_at,
            "stimulus": selected_stimulus,
        }
        
        return TrialResponse.model_validate(trial_dict)
    
    def record_response(self, response_data: ResponseCreate) -> None:
        """
        Record a response to a trial.
        
        Args:
            response_data: Response data
        """
        # Verify trial exists
        trial = self.db.query(Trial).filter(Trial.id == response_data.trial_id).first()
        if not trial:
            raise ValueError(f"Trial {response_data.trial_id} not found")
        
        # Check if response already exists
        existing = (
            self.db.query(Response)
            .filter(Response.trial_id == response_data.trial_id)
            .first()
        )
        if existing:
            raise ValueError(f"Response for trial {response_data.trial_id} already exists")
        
        # Create response
        response = Response(
            trial_id=response_data.trial_id,
            choice=response_data.choice,
            reaction_time_ms=response_data.reaction_time_ms,
            confidence=response_data.confidence,
            created_at=datetime.utcnow(),
        )
        
        self.db.add(response)
        self.db.commit()
    
    def complete_session(self, session_id: str) -> SessionResponse:
        """
        Mark a session as complete.
        
        Args:
            session_id: Session ID
            
        Returns:
            Updated session
        """
        session = self.db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(session)
        
        return SessionResponse.model_validate(session)
    
    def abandon_session(self, session_id: str) -> SessionResponse:
        """
        Mark a session as abandoned.
        
        Args:
            session_id: Session ID
            
        Returns:
            Updated session
        """
        session = self.db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = "abandoned"
        session.completed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(session)
        
        return SessionResponse.model_validate(session)
    
    def get_session_progress(self, session_id: str) -> dict[str, int]:
        """
        Get session progress.
        
        Args:
            session_id: Session ID
            
        Returns:
            Dictionary with progress information
        """
        session = self.db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        total_trials = (
            self.db.query(Trial).filter(Trial.session_id == session_id).count()
        )
        completed_trials = (
            self.db.query(Trial)
            .filter(Trial.session_id == session_id, Trial.response != None)
            .count()
        )
        
        return {
            "total_trials": total_trials,
            "completed_trials": completed_trials,
            "status": session.status,
        }
