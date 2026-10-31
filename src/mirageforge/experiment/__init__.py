"""
Experiment management and analysis.

Provides services for running experiments, collecting responses,
and analyzing results with statistical methods.
"""

from mirageforge.experiment.export import (
    export_study_to_csv,
    export_study_to_json,
    generate_markdown_report,
)
from mirageforge.experiment.service import ExperimentService
from mirageforge.experiment.stats import (
    absolute_difference,
    benjamini_hochberg,
    bootstrap_ci_difference,
    calculate_divergence_metrics,
    jensen_shannon_divergence,
    wilson_ci_proportion,
)

__all__ = [
    "ExperimentService",
    "export_study_to_csv",
    "export_study_to_json",
    "generate_markdown_report",
    "wilson_ci_proportion",
    "bootstrap_ci_difference",
    "jensen_shannon_divergence",
    "absolute_difference",
    "benjamini_hochberg",
    "calculate_divergence_metrics",
]
