"""
Command-line interface for MirageForge.

Provides commands for running demos, initializing databases, starting servers,
and exporting/analyzing data.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from mirageforge import __version__


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="mirageforge",
        description="MirageForge - Visual illusion research platform",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"MirageForge {__version__}",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Demo command
    demo_parser = subparsers.add_parser(
        "demo",
        help="Run synthetic demo pipeline",
    )
    demo_parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/demo"),
        help="Output directory for artifacts",
    )
    demo_parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    demo_parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="Number of search rounds",
    )
    demo_parser.add_argument(
        "--candidates",
        type=int,
        default=200,
        help="Number of candidates per round",
    )
    demo_parser.add_argument(
        "--top",
        type=int,
        default=12,
        help="Number of top candidates to select",
    )
    
    # Init-db command
    subparsers.add_parser(
        "init-db",
        help="Initialize database",
    )
    
    # Run-server command
    server_parser = subparsers.add_parser(
        "run-server",
        help="Start web server",
    )
    server_parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host",
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port",
    )
    server_parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )
    
    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export study data",
    )
    export_parser.add_argument(
        "--study-id",
        type=int,
        required=True,
        help="Study ID to export",
    )
    export_parser.add_argument(
        "--format",
        type=str,
        choices=["csv", "json"],
        default="csv",
        help="Export format",
    )
    export_parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output path",
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze study data",
    )
    analyze_parser.add_argument(
        "--study-id",
        type=int,
        required=True,
        help="Study ID to analyze",
    )
    analyze_parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory for analysis",
    )
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Dispatch to command handlers
    if args.command == "demo":
        run_demo(args)
    elif args.command == "init-db":
        run_init_db(args)
    elif args.command == "run-server":
        run_server(args)
    elif args.command == "export":
        run_export(args)
    elif args.command == "analyze":
        run_analyze(args)


def run_demo(args: argparse.Namespace) -> None:
    """Run synthetic demo pipeline."""
    import logging
    
    from mirageforge.config import get_settings
    from mirageforge.db import get_engine, init_db
    from mirageforge.experiment.export import (
        export_study_to_csv,
        generate_markdown_report,
    )
    from mirageforge.models import ModelRun, Session, Stimulus, Study
    from mirageforge.search import CandidateArchive, CandidateGenerator, UCBAcquisition
    from mirageforge.stimuli.renderer import StimulusRenderer
    from mirageforge.utils.logging import setup_logging
    from mirageforge.vision.mock import MockVisionModel
    from mirageforge.vision.simulated_human import SimulatedHumanModel
    
    setup_logging("INFO")
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 70)
    logger.info("MirageForge Synthetic Demo Pipeline")
    logger.info("=" * 70)
    logger.info("")
    logger.info("⚠️  WARNING: This demo generates SYNTHETIC data")
    logger.info("   No real human participants are involved")
    logger.info("   Results are for demonstration only")
    logger.info("")
    
    # Configuration
    output_dir = args.out
    seed = args.seed
    num_rounds = args.rounds
    candidates_per_round = args.candidates
    top_k = args.top
    
    logger.info(f"Configuration:")
    logger.info(f"  Output directory: {output_dir}")
    logger.info(f"  Random seed: {seed}")
    logger.info(f"  Rounds: {num_rounds}")
    logger.info(f"  Candidates per round: {candidates_per_round}")
    logger.info(f"  Top candidates: {top_k}")
    logger.info("")
    
    # Initialize
    output_dir.mkdir(parents=True, exist_ok=True)
    stimuli_dir = output_dir / "stimuli"
    stimuli_dir.mkdir(exist_ok=True)
    
    # Initialize database
    logger.info("Initializing database...")
    engine = get_engine()
    init_db(engine)
    
    from mirageforge.db import get_db_global
    
    with get_db_global() as db:
        # Create demo study
        study = Study(
            title="MirageForge Synthetic Demo Study",
            version="1.0.0",
            consent_text="This is a SYNTHETIC demo. No real participants are involved.",
            active=True,
            config={
                "trials_per_session": 12,
                "is_synthetic": True,
                "seed": seed,
            },
        )
        db.add(study)
        db.commit()
        db.refresh(study)
        
        logger.info(f"Created study: {study.id} - {study.title}")
        logger.info("")
        
        # Initialize components
        renderer = StimulusRenderer(image_size=512)  # Smaller for demo speed
        generator = CandidateGenerator(seed=seed)
        acquisition = UCBAcquisition(exploration_weight=1.5, seed=seed)
        archive = CandidateArchive()
        
        mock_model = MockVisionModel()
        human_model = SimulatedHumanModel(noise_level=0.15, bias_strength=0.7, seed=seed)
        
        logger.info("Running active search...")
        logger.info("")
        
        # Active search loop
        all_candidates = []
        
        for round_num in range(num_rounds):
            logger.info(f"Round {round_num + 1}/{num_rounds}")
            
            # Generate candidates
            if round_num == 0:
                candidates = generator.generate_random(count=candidates_per_round)
            else:
                # Mutate top candidates from previous round
                top_records = archive.get_top_candidates(count=10)
                top_specs = [r.spec for r in top_records]
                candidates = generator.mutate(
                    top_specs,
                    mutation_rate=0.3,
                    num_mutations=candidates_per_round // len(top_specs),
                )
                # Fill remainder with random
                if len(candidates) < candidates_per_round:
                    extra = generator.generate_random(
                        count=candidates_per_round - len(candidates),
                    )
                    candidates.extend(extra)
            
            logger.info(f"  Generated {len(candidates)} candidates")
            
            # Select candidates using acquisition strategy
            selected = acquisition.select(candidates, count=min(50, len(candidates)))
            logger.info(f"  Selected {len(selected)} for evaluation")
            
            # Evaluate candidates
            for i, spec in enumerate(selected):
                # Render stimulus
                checksum = renderer.render_to_file(spec, stimuli_dir / f"stim_{round_num}_{i}.png")
                
                # Add to archive
                cs = archive.add(spec, round_number=round_num, checksum=checksum)
                
                # Get predictions from both models
                image = renderer.render(spec)
                task_spec = spec.get_task_dict()
                task_spec["stimulus_params"] = spec.get_param_dict()
                task_spec["family"] = spec.family.value
                
                mock_pred = mock_model.predict(image, task_spec)
                human_pred = human_model.predict(image, task_spec)
                
                # Calculate divergence
                from mirageforge.experiment.stats import jensen_shannon_divergence
                import numpy as np
                
                mock_probs = np.array(list(mock_pred["predictions"].values()))
                human_probs = np.array(list(human_pred["predictions"].values()))
                divergence = jensen_shannon_divergence(human_probs, mock_probs)
                
                # Update archive
                archive.update_scores(
                    cs,
                    scores={"mock": float(np.max(mock_probs)), "human": float(np.max(human_probs))},
                    divergence_score=divergence,
                )
                
                all_candidates.append((spec, checksum, divergence))
            
            logger.info(f"  Evaluated {len(selected)} candidates")
            logger.info("")
        
        # Select top candidates
        logger.info(f"Selecting top {top_k} candidates...")
        top_records = archive.get_top_candidates(count=top_k)
        
        for record in top_records:
            archive.mark_selected(record.checksum)
            
            # Add to database
            stimulus = Stimulus(
                study_id=study.id,
                family=record.spec.family.value,
                params=record.spec.get_param_dict(),
                seed=record.spec.seed,
                image_path=str(stimuli_dir / f"selected_{record.checksum[:8]}.png"),
                sha256=record.checksum,
                task_spec=record.spec.get_task_dict(),
                intended_effect="Candidate stimulus for validation",
                safety_flags=record.spec.get_safety_dict(),
            )
            db.add(stimulus)
            db.commit()  # Commit to get stimulus.id
            db.refresh(stimulus)
            
            # Render if not already rendered
            if not Path(stimulus.image_path).exists():
                renderer.render_to_file(record.spec, Path(stimulus.image_path))
            
            # Add model runs
            image = renderer.render(record.spec)
            task_spec = record.spec.get_task_dict()
            task_spec["stimulus_params"] = record.spec.get_param_dict()
            task_spec["family"] = record.spec.family.value
            
            mock_pred = mock_model.predict(image, task_spec)
            human_pred = human_model.predict(image, task_spec)
            
            mock_run = ModelRun(
                model_name=mock_model.name,
                model_version=mock_model.version,
                stimulus_id=stimulus.id,
                probe=task_spec,
                scores=mock_pred,
            )
            db.add(mock_run)
            
            human_run = ModelRun(
                model_name=human_model.name,
                model_version=human_model.version,
                stimulus_id=stimulus.id,
                probe=task_spec,
                scores=human_pred,
            )
            db.add(human_run)
        
        db.commit()
        logger.info(f"Added {len(top_records)} selected stimuli to database")
        logger.info("")
        
        # Run synthetic experiment
        logger.info("Running synthetic experiment...")
        from mirageforge.experiment.service import ExperimentService
        from mirageforge.schemas import ExperimentConfig, ResponseCreate, SessionCreate
        
        service = ExperimentService(db)
        
        # Create synthetic session
        session_data = SessionCreate(study_id=study.id, consent_version="1.0.0")
        session = service.create_session(session_data)
        
        config = ExperimentConfig(study_id=study.id, trials_count=12)
        
        # Simulate trials
        for trial_num in range(12):
            trial = service.get_next_trial(session.id, config)
            if trial is None:
                break
            
            # Simulate response
            import random
            options = list(trial.option_order.keys())
            choice = random.choice(options)
            reaction_time = random.randint(500, 3000)
            
            response_data = ResponseCreate(
                trial_id=trial.id,
                choice=choice,
                reaction_time_ms=reaction_time,
            )
            service.record_response(response_data)
        
        # Complete session
        service.complete_session(session.id)
        logger.info(f"Completed synthetic session: {session.id}")
        logger.info("")
        
        # Export data
        logger.info("Exporting data...")
        csv_files = export_study_to_csv(db, study.id, output_dir)
        logger.info(f"  Exported CSV files: {list(csv_files.keys())}")
        
        # Generate report
        report_file = output_dir / "report.md"
        generate_markdown_report(db, study.id, report_file, is_synthetic=True)
        logger.info(f"  Generated report: {report_file}")
        
        # Generate HTML gallery
        logger.info("Generating HTML gallery...")
        gallery_file = output_dir / "index.html"
        _generate_html_gallery(top_records, stimuli_dir, gallery_file)
        logger.info(f"  Generated gallery: {gallery_file}")
        
        # Generate metrics JSON
        metrics_file = output_dir / "metrics.json"
        stats = archive.get_stats()
        stats["is_synthetic"] = True
        stats["demo_seed"] = seed
        with open(metrics_file, "w") as f:
            json.dump(stats, f, indent=2)
        logger.info(f"  Generated metrics: {metrics_file}")
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("Demo completed successfully!")
        logger.info("=" * 70)
        logger.info("")
        logger.info("Artifacts:")
        logger.info(f"  - Stimuli: {stimuli_dir}")
        logger.info(f"  - Gallery: {gallery_file}")
        logger.info(f"  - Report: {report_file}")
        logger.info(f"  - Metrics: {metrics_file}")
        logger.info("")
        logger.info("⚠️  Remember: All results are SYNTHETIC")
        logger.info("")


def _generate_html_gallery(
    records: list,
    stimuli_dir: Path,
    output_file: Path,
) -> None:
    """Generate HTML gallery for selected stimuli."""
    html_lines = []
    html_lines.append("<!DOCTYPE html>")
    html_lines.append("<html lang='en'>")
    html_lines.append("<head>")
    html_lines.append("  <meta charset='UTF-8'>")
    html_lines.append("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html_lines.append("  <title>MirageForge Demo Gallery - SYNTHETIC</title>")
    html_lines.append("  <style>")
    html_lines.append("    body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }")
    html_lines.append("    .warning { background: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px; }")
    html_lines.append("    .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }")
    html_lines.append("    .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }")
    html_lines.append("    .card img { width: 100%; height: auto; border-radius: 4px; }")
    html_lines.append("    .card h3 { margin: 10px 0 5px 0; }")
    html_lines.append("    .card p { margin: 5px 0; font-size: 14px; color: #666; }")
    html_lines.append("  </style>")
    html_lines.append("</head>")
    html_lines.append("<body>")
    html_lines.append("  <h1>MirageForge Demo Gallery</h1>")
    html_lines.append("  <div class='warning'>")
    html_lines.append("    <strong>⚠️ SYNTHETIC DATA WARNING</strong><br>")
    html_lines.append("    This gallery contains SYNTHETIC candidate stimuli generated by AI.")
    html_lines.append("    No real human validation has been performed.")
    html_lines.append("    These are candidates for future research, not validated illusions.")
    html_lines.append("  </div>")
    html_lines.append("  <div class='gallery'>")
    
    for i, record in enumerate(records):
        image_name = f"selected_{record.checksum[:8]}.png"
        image_path = stimuli_dir / image_name
        
        # Use relative path for HTML
        rel_path = f"stimuli/{image_name}"
        
        html_lines.append("    <div class='card'>")
        html_lines.append(f"      <img src='{rel_path}' alt='Stimulus {i+1}'>")
        html_lines.append(f"      <h3>Candidate {i+1}</h3>")
        html_lines.append(f"      <p><strong>Family:</strong> {record.spec.family.value}</p>")
        html_lines.append(f"      <p><strong>Seed:</strong> {record.spec.seed}</p>")
        html_lines.append(f"      <p><strong>Divergence:</strong> {record.divergence_score:.4f}</p>")
        html_lines.append(f"      <p><strong>Checksum:</strong> {record.checksum[:16]}...</p>")
        html_lines.append("    </div>")
    
    html_lines.append("  </div>")
    html_lines.append("  <footer style='margin-top: 40px; padding: 20px; text-align: center; color: #666;'>")
    html_lines.append("    <p>Generated by MirageForge Demo Pipeline</p>")
    html_lines.append("    <p>All stimuli and results are SYNTHETIC - for demonstration only</p>")
    html_lines.append("  </footer>")
    html_lines.append("</body>")
    html_lines.append("</html>")
    
    with open(output_file, "w") as f:
        f.write("\n".join(html_lines))


def run_init_db(args: argparse.Namespace) -> None:
    """Initialize database."""
    from mirageforge.db import get_engine, init_db
    from mirageforge.utils.logging import setup_logging
    
    setup_logging("INFO")
    
    print("Initializing database...")
    engine = get_engine()
    init_db(engine)
    print("✓ Database initialized successfully")


def run_server(args: argparse.Namespace) -> None:
    """Start web server."""
    import uvicorn
    
    from mirageforge.utils.logging import setup_logging
    
    setup_logging("INFO")
    
    print(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(
        "mirageforge.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


def run_export(args: argparse.Namespace) -> None:
    """Export study data."""
    from mirageforge.config import get_settings
    from mirageforge.db import get_db_global
    from mirageforge.experiment.export import export_study_to_csv, export_study_to_json
    from mirageforge.utils.logging import setup_logging
    
    setup_logging("INFO")
    
    settings = get_settings()
    
    # Check admin token if required
    if settings.is_admin_enabled():
        print("Admin token required for export")
        # In real implementation, would prompt for token
    
    with get_db_global() as db:
        if args.format == "csv":
            files = export_study_to_csv(db, args.study_id, args.out)
            print(f"✓ Exported CSV files to {args.out}")
            for name, path in files.items():
                print(f"  - {name}: {path}")
        elif args.format == "json":
            export_study_to_json(db, args.study_id, args.out)
            print(f"✓ Exported JSON to {args.out}")


def run_analyze(args: argparse.Namespace) -> None:
    """Analyze study data."""
    from mirageforge.db import get_db_global
    from mirageforge.experiment.export import generate_markdown_report
    from mirageforge.utils.logging import setup_logging
    
    setup_logging("INFO")
    
    args.out.mkdir(parents=True, exist_ok=True)
    report_file = args.out / "analysis_report.md"
    
    with get_db_global() as db:
        generate_markdown_report(db, args.study_id, report_file, is_synthetic=False)
    
    print(f"✓ Analysis report generated: {report_file}")


if __name__ == "__main__":
    main()
