"""
Candidate archive for tracking search history.

Stores candidates, their scores, and evaluation history.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from mirageforge.stimuli.dsl import StimulusSpec
from mirageforge.utils.hashing import hash_dict


@dataclass
class CandidateRecord:
    """Record of a candidate stimulus with evaluation history."""
    
    spec: StimulusSpec
    checksum: str
    round_number: int
    scores: dict[str, float] = field(default_factory=dict)
    divergence_score: Optional[float] = None
    selected: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self) -> None:
        """Calculate checksum if not provided."""
        if not self.checksum:
            param_dict = self.spec.get_param_dict()
            self.checksum = hash_dict({
                "family": self.spec.family.value,
                "params": param_dict,
                "seed": self.spec.seed,
            })


class CandidateArchive:
    """
    Archive for storing candidates and their evaluation history.
    
    Tracks all candidates generated during search, their scores,
    and which rounds they participated in.
    """
    
    def __init__(self):
        """Initialize empty archive."""
        self.records: dict[str, CandidateRecord] = {}
        self.rounds: dict[int, list[str]] = {}  # round_number -> list of checksums
        self.selected: list[str] = []  # checksums of selected candidates
    
    def add(
        self,
        spec: StimulusSpec,
        round_number: int,
        checksum: str = "",
        scores: Optional[dict[str, float]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Add a candidate to the archive.
        
        Args:
            spec: Stimulus specification
            round_number: Search round number
            checksum: Optional checksum (calculated if not provided)
            scores: Optional initial scores
            metadata: Optional metadata
            
        Returns:
            Checksum of the candidate
        """
        record = CandidateRecord(
            spec=spec,
            checksum=checksum,
            round_number=round_number,
            scores=scores or {},
            metadata=metadata or {},
        )
        
        # Add to records
        self.records[record.checksum] = record
        
        # Add to round
        if round_number not in self.rounds:
            self.rounds[round_number] = []
        if record.checksum not in self.rounds[round_number]:
            self.rounds[round_number].append(record.checksum)
        
        return record.checksum
    
    def update_scores(
        self,
        checksum: str,
        scores: dict[str, float],
        divergence_score: Optional[float] = None,
    ) -> None:
        """
        Update scores for a candidate.
        
        Args:
            checksum: Candidate checksum
            scores: New scores
            divergence_score: Optional divergence metric
        """
        if checksum in self.records:
            self.records[checksum].scores.update(scores)
            if divergence_score is not None:
                self.records[checksum].divergence_score = divergence_score
    
    def mark_selected(self, checksum: str) -> None:
        """
        Mark a candidate as selected for final set.
        
        Args:
            checksum: Candidate checksum
        """
        if checksum in self.records:
            self.records[checksum].selected = True
            if checksum not in self.selected:
                self.selected.append(checksum)
    
    def get(self, checksum: str) -> Optional[CandidateRecord]:
        """
        Get a candidate record by checksum.
        
        Args:
            checksum: Candidate checksum
            
        Returns:
            CandidateRecord or None
        """
        return self.records.get(checksum)
    
    def get_by_round(self, round_number: int) -> list[CandidateRecord]:
        """
        Get all candidates from a specific round.
        
        Args:
            round_number: Round number
            
        Returns:
            List of candidate records
        """
        checksums = self.rounds.get(round_number, [])
        return [self.records[cs] for cs in checksums if cs in self.records]
    
    def get_selected(self) -> list[CandidateRecord]:
        """
        Get all selected candidates.
        
        Returns:
            List of selected candidate records
        """
        return [self.records[cs] for cs in self.selected if cs in self.records]
    
    def get_top_candidates(
        self,
        count: int,
        sort_by: str = "divergence_score",
    ) -> list[CandidateRecord]:
        """
        Get top candidates by score.
        
        Args:
            count: Number of candidates to return
            sort_by: Score key to sort by
            
        Returns:
            List of top candidate records
        """
        # Filter candidates that have the score
        candidates_with_score = [
            r for r in self.records.values()
            if sort_by == "divergence_score" and r.divergence_score is not None
            or sort_by in r.scores
        ]
        
        # Sort by score
        if sort_by == "divergence_score":
            sorted_candidates = sorted(
                candidates_with_score,
                key=lambda r: r.divergence_score or 0.0,
                reverse=True,
            )
        else:
            sorted_candidates = sorted(
                candidates_with_score,
                key=lambda r: r.scores.get(sort_by, 0.0),
                reverse=True,
            )
        
        return sorted_candidates[:count]
    
    def get_stats(self) -> dict[str, Any]:
        """
        Get archive statistics.
        
        Returns:
            Dictionary with archive stats
        """
        total = len(self.records)
        selected = len(self.selected)
        rounds = len(self.rounds)
        
        # Calculate average scores
        divergence_scores = [
            r.divergence_score for r in self.records.values()
            if r.divergence_score is not None
        ]
        
        return {
            "total_candidates": total,
            "selected_candidates": selected,
            "total_rounds": rounds,
            "avg_divergence_score": (
                sum(divergence_scores) / len(divergence_scores)
                if divergence_scores else 0.0
            ),
            "max_divergence_score": max(divergence_scores) if divergence_scores else 0.0,
        }
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert archive to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return {
            "records": {
                cs: {
                    "family": record.spec.family.value,
                    "params": record.spec.get_param_dict(),
                    "seed": record.spec.seed,
                    "round": record.round_number,
                    "scores": record.scores,
                    "divergence_score": record.divergence_score,
                    "selected": record.selected,
                    "checksum": record.checksum,
                }
                for cs, record in self.records.items()
            },
            "rounds": self.rounds,
            "selected": self.selected,
            "stats": self.get_stats(),
        }
