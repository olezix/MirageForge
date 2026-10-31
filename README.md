# MirageForge

**Open research platform for AI-driven discovery of candidate visual illusions**

MirageForge is a platform that generates parameterized visual stimuli, runs perception experiments with human participants (or synthetic simulators), compares human responses with vision model predictions, and identifies candidate stimuli that maximize human-model divergence.

## ⚠️ Important Disclaimers

- **This is a research platform, not a medical tool.** It does not diagnose or treat any conditions.
- **Demo results are SYNTHETIC.** The demo pipeline uses simulated human responses, not real participants.
- **No illusions are "discovered" without real validation.** Candidate stimuli require validation with real human participants and ethical approval.
- **Participation is 18+ only.** Real experiments require informed consent and ethical oversight.

## Features

- **5 Stimulus Families**: Size context, line context, contrast, crowding, and grating detection
- **Active Search**: UCB and diversity-based acquisition strategies for efficient exploration
- **Vision Backends**: Mock model, simulated human, and optional CLIP integration
- **Web Experiments**: FastAPI-based platform for running perception experiments
- **Statistical Analysis**: Wilson CI, bootstrap, Jensen-Shannon divergence, Benjamini-Hochberg correction
- **Privacy by Design**: Anonymous sessions, no PII collection, no tracking
- **Reproducible**: Deterministic rendering with SHA256 checksums and fixed seeds

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/mirageforge/mirageforge.git
cd mirageforge

# Setup (installs dependencies)
make setup

# Initialize database
make init-db
```

### Run Demo

The demo generates synthetic candidate stimuli and runs a simulated experiment:

```bash
make demo
```

This creates:
- `artifacts/demo/stimuli/` - Generated PNG stimuli
- `artifacts/demo/index.html` - Interactive gallery
- `artifacts/demo/report.md` - Analysis report (marked SYNTHETIC)
- `artifacts/demo/metrics.json` - Statistics and metadata

### Run Web Server

```bash
make run
```

Visit `http://localhost:8000` to:
- View landing page with information
- Participate in experiments (after consent)
- View gallery of candidate stimuli
- See aggregate dashboard statistics

### Run Tests

```bash
make test
```

### Run All Checks

```bash
make check  # lint + test + demo smoke test
```

## Project Structure

```
MirageForge/
├── src/mirageforge/
│   ├── stimuli/          # Stimulus DSL and renderer
│   │   ├── dsl.py        # Parameterized stimulus specifications
│   │   ├── renderer.py   # Pillow-based rendering
│   │   ├── safety.py     # Safety validation
│   │   └── generators/   # Family-specific generators
│   ├── vision/           # Vision model backends
│   │   ├── base.py       # Abstract interface
│   │   ├── mock.py       # Mock model (deterministic pseudo-scores)
│   │   ├── simulated_human.py  # Synthetic human simulator
│   │   └── clip_backend.py     # Optional CLIP integration
│   ├── search/           # Active search algorithms
│   │   ├── candidates.py # Candidate generation and mutation
│   │   ├── acquisition.py # UCB, random, diversity strategies
│   │   └── archive.py    # Candidate tracking
│   ├── experiment/       # Experiment management
│   │   ├── service.py    # Session and trial management
│   │   ├── stats.py      # Statistical analysis
│   │   └── export.py     # CSV/JSON/report export
│   ├── web/              # FastAPI web application
│   │   ├── app.py        # Routes and endpoints
│   │   ├── templates/    # HTML templates
│   │   └── static/       # Static files
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── config.py         # Configuration management
│   ├── db.py             # Database utilities
│   └── cli.py            # Command-line interface
├── tests/                # Test suite
├── docs/                 # Documentation
├── artifacts/            # Generated outputs (not in git)
└── data/                 # Database files (not in git)
```

## CLI Commands

```bash
# Run synthetic demo
python -m mirageforge.cli demo --out artifacts/demo --seed 42 --rounds 3 --candidates 200 --top 12

# Initialize database
python -m mirageforge.cli init-db

# Start web server
python -m mirageforge.cli run-server --host 0.0.0.0 --port 8000

# Export study data (requires admin token)
python -m mirageforge.cli export --study-id 1 --format csv --out artifacts/export

# Analyze study results
python -m mirageforge.cli analyze --study-id 1 --out artifacts/analysis
```

## Stimulus Families

1. **Size Context** (Ebbinghaus-like): Tests size perception with surrounding context
2. **Line Context** (Müller-Lyer-like): Tests line length perception with arrows/fins
3. **Contrast**: Tests brightness and color perception with surrounds
4. **Crowding**: Tests object recognition with flanking stimuli
5. **Grating**: Tests contrast sensitivity and detection thresholds

All stimuli are:
- Static (no animation or flashing)
- Deterministic (same seed → same image)
- Safe (validated against photosensitivity guidelines)
- Reproducible (SHA256 checksums)

## Vision Backends

### MockVisionModel
- **Required**: Always available, no dependencies
- **Purpose**: Testing and demonstration
- **Output**: Deterministic pseudo-scores based on image hash
- **Note**: Clearly marked as MOCK

### SimulatedHumanModel
- **Required**: Always available
- **Purpose**: Synthetic human responses for demo
- **Output**: Biased responses based on parameterized psychometric functions
- **Note**: Clearly marked as SYNTHETIC

### CLIPVisionBackend (Optional)
- **Dependencies**: `torch`, `transformers`
- **Purpose**: Real vision model predictions
- **Output**: Image-text similarity scores
- **Note**: Gracefully degrades if unavailable

## Statistical Methods

- **Wilson Confidence Intervals**: For choice proportions
- **Bootstrap CI**: For human-model divergence
- **Jensen-Shannon Divergence**: Distribution comparison
- **Benjamini-Hochberg**: Multiple comparison correction
- **Chi-squared Tests**: Goodness of fit

## Privacy and Ethics

- **No PII**: No IP addresses, user agents, names, or emails collected
- **Anonymous Sessions**: UUID tokens only
- **Informed Consent**: Required before participation
- **18+ Only**: Age verification required
- **Stop Anytime**: Participants can withdraw at any point
- **No Tracking**: No analytics, no external services
- **Local Only**: All data stored locally, no cloud uploads

## Limitations

- **Synthetic Demo**: Demo uses simulated humans, not real participants
- **Small Sample**: Default demo has limited statistical power
- **Online vs Lab**: Web experiments differ from controlled lab settings
- **Not Validated**: Platform requires real validation before research use
- **Limited Families**: Only 5 stimulus families implemented
- **No Medical Claims**: Not a diagnostic or treatment tool

## What Cannot Be Claimed

Based on synthetic demo results, we **cannot** claim:
- That new illusions have been discovered
- That specific stimuli cause specific perceptual effects
- That the platform is validated for research
- Any medical or diagnostic conclusions

Real validation requires:
1. Ethical approval from IRB/ethics committee
2. Real human participants with informed consent
3. Controlled experimental protocols
4. Appropriate statistical analysis
5. Peer review and publication

## Documentation

- `docs/ethics.md` - Ethical considerations
- `docs/protocol.md` - Research protocol template
- `docs/limitations.md` - Detailed limitations
- `docs/science.md` - Scientific methodology
- `docs/privacy.md` - Privacy policy
- `docs/accessibility.md` - Accessibility features
- `docs/model_cards/` - Vision model documentation
- `PORTFOLIO.md` - Project overview for portfolio
- `FINAL_REPORT.md` - Implementation report

## Development

### Requirements

- Python 3.11+
- pip, setuptools, wheel

### Setup Development Environment

```bash
make setup        # Install all dependencies
make lint         # Run linters (ruff, mypy)
make test         # Run tests
make format       # Format code
```

### Docker

```bash
make docker       # Build and run with docker-compose
make docker-build # Build image only
```

### CI/CD

GitHub Actions workflow runs on push/PR:
- Lint with ruff
- Type check with mypy
- Run tests with pytest
- Run demo smoke test

## Contributing

See `CONTRIBUTING.md` for guidelines.

## License

- **Code**: MIT License (see `LICENSE`)
- **Data**: See `DATA_LICENSE.md`
- **Stimuli**: Generated programmatically, no external assets

## Citation

```bibtex
@software{mirageforge2024,
  title = {MirageForge: Open research platform for visual illusion discovery},
  author = {olezix},
  year = {2024},
  url = {https://github.com/mirageforge/mirageforge}
}
```

## Acknowledgments

This project is inspired by research in visual perception, psychophysics, and active learning. It is a portfolio/demonstration project and is not affiliated with any academic institution.

## Contact

For questions or issues, please open a GitHub issue.

---

**Remember**: All demo results are SYNTHETIC. Real research requires real participants and ethical approval.
