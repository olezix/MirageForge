"""
Active search for candidate stimuli.

Implements candidate generation, novelty/diversity metrics,
and acquisition strategies for identifying interesting stimuli.
"""

from mirageforge.search.acquisition import (
    AcquisitionStrategy,
    DiversityAcquisition,
    RandomAcquisition,
    UCBAcquisition,
)
from mirageforge.search.archive import CandidateArchive
from mirageforge.search.candidates import (
    CandidateGenerator,
    generate_candidates,
    mutate_candidates,
)

__all__ = [
    "CandidateGenerator",
    "generate_candidates",
    "mutate_candidates",
    "AcquisitionStrategy",
    "RandomAcquisition",
    "UCBAcquisition",
    "DiversityAcquisition",
    "CandidateArchive",
]
