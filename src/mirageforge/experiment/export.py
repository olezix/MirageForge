"""
Data export utilities for studies and experiments.

Exports data to CSV, JSON, and generates reports in markdown/HTML.
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session as DBSession

from mirageforge.models import ModelRun, Response, Session, Stimulus, Study, Trial


def export_study_to_csv(
    db: DBSession,
    study_id: int,
    output_dir: Path,
) -> dict[str, Path]:
    """
    Export study data to CSV files.

    Args:
        db: Database session
        study_id: Study ID to export
        output_dir: Output directory

    Returns:
        Dictionary mapping file type to file path
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get study
    study = db.query(Study).filter(Study.id == study_id).first()
    if not study:
        raise ValueError(f"Study {study_id} not found")

    files = {}

    # Export stimuli
    stimuli = db.query(Stimulus).filter(Stimulus.study_id == study_id).all()
    stimuli_file = output_dir / f"study_{study_id}_stimuli.csv"
    with open(stimuli_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "family",
                "params",
                "seed",
                "image_path",
                "sha256",
                "task_spec",
                "intended_effect",
                "created_at",
            ]
        )
        for s in stimuli:
            writer.writerow(
                [
                    s.id,
                    s.family,
                    json.dumps(s.params),
                    s.seed,
                    s.image_path,
                    s.sha256,
                    json.dumps(s.task_spec),
                    s.intended_effect,
                    s.created_at,
                ]
            )
    files["stimuli"] = stimuli_file

    # Export sessions
    sessions = db.query(Session).filter(Session.study_id == study_id).all()
    sessions_file = output_dir / f"study_{study_id}_sessions.csv"
    with open(sessions_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "consent_version", "status", "created_at", "completed_at"])
        for sess in sessions:
            writer.writerow(
                [
                    sess.id,
                    sess.consent_version,
                    sess.status,
                    sess.created_at,
                    sess.completed_at,
                ]
            )
    files["sessions"] = sessions_file

    # Export responses
    session_ids = [s.id for s in sessions]
    if session_ids:
        trials = db.query(Trial).filter(Trial.session_id.in_(session_ids)).all()
        trial_ids = [t.id for t in trials]

        if trial_ids:
            responses = db.query(Response).filter(Response.trial_id.in_(trial_ids)).all()
            responses_file = output_dir / f"study_{study_id}_responses.csv"
            with open(responses_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "response_id",
                        "trial_id",
                        "session_id",
                        "stimulus_id",
                        "choice",
                        "reaction_time_ms",
                        "confidence",
                        "created_at",
                    ]
                )
                for r in responses:
                    trial = db.query(Trial).filter(Trial.id == r.trial_id).first()
                    writer.writerow(
                        [
                            r.id,
                            r.trial_id,
                            trial.session_id,
                            trial.stimulus_id,
                            r.choice,
                            r.reaction_time_ms,
                            r.confidence,
                            r.created_at,
                        ]
                    )
            files["responses"] = responses_file

    # Export model runs
    stimulus_ids = [s.id for s in stimuli]
    if stimulus_ids:
        model_runs = db.query(ModelRun).filter(ModelRun.stimulus_id.in_(stimulus_ids)).all()
        if model_runs:
            model_file = output_dir / f"study_{study_id}_model_runs.csv"
            with open(model_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "id",
                        "model_name",
                        "model_version",
                        "stimulus_id",
                        "probe",
                        "scores",
                        "created_at",
                    ]
                )
                for m in model_runs:
                    writer.writerow(
                        [
                            m.id,
                            m.model_name,
                            m.model_version,
                            m.stimulus_id,
                            json.dumps(m.probe),
                            json.dumps(m.scores),
                            m.created_at,
                        ]
                    )
            files["model_runs"] = model_file

    return files


def export_study_to_json(
    db: DBSession,
    study_id: int,
    output_file: Path,
) -> dict[str, Any]:
    """
    Export study data to JSON.

    Args:
        db: Database session
        study_id: Study ID
        output_file: Output file path

    Returns:
        Exported data dictionary
    """
    study = db.query(Study).filter(Study.id == study_id).first()
    if not study:
        raise ValueError(f"Study {study_id} not found")

    # Build export data
    data = {
        "study": {
            "id": study.id,
            "title": study.title,
            "version": study.version,
            "created_at": study.created_at.isoformat(),
            "config": study.config,
        },
        "stimuli": [],
        "sessions": [],
        "responses": [],
        "model_runs": [],
        "exported_at": datetime.utcnow().isoformat(),
    }

    # Export stimuli
    stimuli = db.query(Stimulus).filter(Stimulus.study_id == study_id).all()
    for s in stimuli:
        data["stimuli"].append(
            {
                "id": s.id,
                "family": s.family,
                "params": s.params,
                "seed": s.seed,
                "sha256": s.sha256,
                "task_spec": s.task_spec,
            }
        )

    # Export sessions and responses
    sessions = db.query(Session).filter(Session.study_id == study_id).all()
    for sess in sessions:
        data["sessions"].append(
            {
                "id": sess.id,
                "status": sess.status,
                "created_at": sess.created_at.isoformat(),
                "completed_at": sess.completed_at.isoformat() if sess.completed_at else None,
            }
        )

    # Export responses (anonymized)
    session_ids = [s.id for s in sessions]
    if session_ids:
        trials = db.query(Trial).filter(Trial.session_id.in_(session_ids)).all()
        for trial in trials:
            response = db.query(Response).filter(Response.trial_id == trial.id).first()
            if response:
                data["responses"].append(
                    {
                        "trial_id": trial.id,
                        "session_id": trial.session_id,
                        "stimulus_id": trial.stimulus_id,
                        "choice": response.choice,
                        "reaction_time_ms": response.reaction_time_ms,
                        "confidence": response.confidence,
                    }
                )

    # Export model runs
    stimulus_ids = [s.id for s in stimuli]
    if stimulus_ids:
        model_runs = db.query(ModelRun).filter(ModelRun.stimulus_id.in_(stimulus_ids)).all()
        for m in model_runs:
            data["model_runs"].append(
                {
                    "model_name": m.model_name,
                    "model_version": m.model_version,
                    "stimulus_id": m.stimulus_id,
                    "scores": m.scores,
                }
            )

    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data


def generate_markdown_report(
    db: DBSession,
    study_id: int,
    output_file: Path,
    is_synthetic: bool = True,
) -> str:
    """
    Generate markdown report for a study.

    Args:
        db: Database session
        study_id: Study ID
        output_file: Output file path
        is_synthetic: Whether data is synthetic

    Returns:
        Report content
    """
    study = db.query(Study).filter(Study.id == study_id).first()
    if not study:
        raise ValueError(f"Study {study_id} not found")

    # Gather statistics
    sessions = db.query(Session).filter(Session.study_id == study_id).all()
    total_sessions = len(sessions)
    completed_sessions = len([s for s in sessions if s.status == "completed"])

    stimuli = db.query(Stimulus).filter(Stimulus.study_id == study_id).all()
    total_stimuli = len(stimuli)

    # Build report
    lines = []
    lines.append(f"# Study Report: {study.title}")
    lines.append("")
    lines.append(f"**Study ID:** {study_id}")
    lines.append(f"**Version:** {study.version}")
    lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append("")

    if is_synthetic:
        lines.append("## ⚠️ SYNTHETIC DATA WARNING")
        lines.append("")
        lines.append("**This report contains SYNTHETIC data generated by a simulator.**")
        lines.append("These results are for demonstration purposes only and do not represent")
        lines.append(
            "real human participants. No scientific conclusions should be drawn from this data."
        )
        lines.append("")

    lines.append("## Summary Statistics")
    lines.append("")
    lines.append(f"- **Total Sessions:** {total_sessions}")
    lines.append(f"- **Completed Sessions:** {completed_sessions}")
    lines.append(f"- **Total Stimuli:** {total_stimuli}")
    lines.append("")

    lines.append("## Stimulus Families")
    lines.append("")
    family_counts = {}
    for s in stimuli:
        family_counts[s.family] = family_counts.get(s.family, 0) + 1
    for family, count in sorted(family_counts.items()):
        lines.append(f"- **{family}:** {count} stimuli")
    lines.append("")

    lines.append("## Limitations")
    lines.append("")
    if is_synthetic:
        lines.append("- All responses are synthetic, generated by a simulated human model")
        lines.append("- No real human participants were involved")
        lines.append("- Results cannot be generalized to human perception")
    lines.append("- Online experiments may differ from laboratory conditions")
    lines.append("- Small sample sizes may limit statistical power")
    lines.append("- This is not a medical or diagnostic tool")
    lines.append("")

    lines.append("## What Cannot Be Claimed")
    lines.append("")
    lines.append("Based on this data, we **cannot** claim:")
    lines.append("- That new illusions have been discovered")
    lines.append("- That specific stimuli cause specific perceptual effects in humans")
    lines.append("- That the platform is validated for research use")
    lines.append("- Any medical or diagnostic conclusions")
    lines.append("")
    lines.append("Real validation with human participants and ethical approval is required.")
    lines.append("")

    lines.append("## Next Steps for Real Validation")
    lines.append("")
    lines.append("1. Obtain ethical approval from an IRB or ethics committee")
    lines.append("2. Recruit real human participants with informed consent")
    lines.append("3. Conduct controlled experiments with proper protocols")
    lines.append("4. Analyze results with appropriate statistical methods")
    lines.append("5. Peer review and publication")
    lines.append("")

    report_content = "\n".join(lines)

    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    return report_content
