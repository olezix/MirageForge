# MirageForge Implementation Plan

## Overview
MirageForge is an open research platform for AI-driven discovery and validation of candidate visual illusions, measuring divergence between human perception and vision models.

## Implementation Stages

### Stage 1: Project Setup ✓
- [x] Create PLAN.md and ASSUMPTIONS.md
- [ ] Configure pyproject.toml with dependencies
- [ ] Setup Makefile with standard commands
- [ ] Configure .gitignore, .env.example
- [ ] Setup ruff and mypy configuration
- [ ] Create basic directory structure
- [ ] Initial commit

### Stage 2: Core Domain Models
- [ ] Define SQLAlchemy models (Study, Stimulus, Session, Trial, Response, ModelRun, AuditEvent)
- [ ] Create Pydantic schemas for validation
- [ ] Implement database initialization (init-db command)
- [ ] Setup database migrations via SQLAlchemy create_all
- [ ] Implement export utilities
- [ ] Tests for models

### Stage 3: Stimulus DSL and Renderer
- [ ] Define StimulusSpec DSL with Pydantic v2
- [ ] Implement safety checks for parameters
- [ ] Create renderer with Pillow + numpy
- [ ] Implement 5 stimulus families:
  1. Geometric size context (Ebbinghaus-like)
  2. Geometric line context (Müller-Lyer/Poggendorff-like)
  3. Simultaneous contrast/color context
  4. Crowding/flanking context
  5. Grating detection/threshold contrast
- [ ] Deterministic rendering with SHA256 checksums
- [ ] Tests for determinism and safety

### Stage 4: Vision Backends
- [ ] Define VisionBackend interface
- [ ] Implement MockVisionModel (required, no network/GPU)
- [ ] Implement SimulatedHumanModel (required, synthetic)
- [ ] Implement CLIPVisionBackend (optional, lazy loading)
- [ ] Create model cards documentation
- [ ] Tests for all backends

### Stage 5: Active Search System
- [ ] Implement candidate generator with parameter mutations
- [ ] Implement novelty/diversity via parameter binning
- [ ] Implement acquisition strategies (Random, UCB)
- [ ] Create candidate archive with history
- [ ] Fixed seeds and experiment configuration
- [ ] Tests for search algorithms

### Stage 6: CLI Demo Command
- [ ] Implement demo command
- [ ] Generate candidates
- [ ] Run active selection
- [ ] Render 50+ PNG stimuli
- [ ] Run synthetic experiment with SimulatedHumanModel
- [ ] Compare with MockVisionModel
- [ ] Calculate statistics
- [ ] Generate artifacts (HTML gallery, CSV, JSON, markdown report)
- [ ] Mark all outputs as SYNTHETIC
- [ ] Tests for CLI

### Stage 7: FastAPI Web Application
- [ ] Setup FastAPI app with Jinja2
- [ ] Implement routes:
  - GET / (landing page)
  - GET /consent (consent form)
  - GET /experiment (trials)
  - POST /api/session (create session)
  - POST /api/trial (get next trial)
  - POST /api/response (save response)
  - POST /api/complete (complete session)
  - GET /debrief (explanation)
  - GET /dashboard (aggregate metrics)
  - GET /gallery (candidate stimuli)
  - GET /healthz (health check)
  - Admin endpoints (with ADMIN_TOKEN)
- [ ] Implement consent flow
- [ ] Implement experiment flow (10-20 trials)
- [ ] Randomization and balanced option order
- [ ] Security headers (CSP, X-Content-Type-Options, etc.)
- [ ] CSRF protection
- [ ] Rate limiting (in-memory, no IP storage)
- [ ] Accessibility (ARIA, alt text, keyboard navigation)
- [ ] Responsive design (mobile + desktop)
- [ ] Tests for API endpoints

### Stage 8: Statistics and Reporting
- [ ] Implement Wilson 95% CI for proportions
- [ ] Implement bootstrap CI for divergence
- [ ] Calculate absolute difference and Jensen-Shannon divergence
- [ ] Implement Benjamini-Hochberg correction
- [ ] Generate CSV, JSON, HTML/markdown reports
- [ ] Mark SYNTHETIC data explicitly
- [ ] Save seeds, versions, configs, checksums
- [ ] Tests for statistics

### Stage 9: Documentation
- [ ] README.md with reproduction instructions
- [ ] docs/ethics.md
- [ ] docs/protocol.md
- [ ] docs/consent_template.md
- [ ] docs/irb_checklist.md
- [ ] docs/limitations.md
- [ ] docs/datasheet.md
- [ ] docs/model_cards/ (for each backend)
- [ ] docs/privacy.md
- [ ] docs/accessibility.md
- [ ] docs/reproduction.md
- [ ] docs/science.md
- [ ] PORTFOLIO.md
- [ ] LICENSE (MIT)
- [ ] DATA_LICENSE.md
- [ ] CITATION.cff
- [ ] CONTRIBUTING.md
- [ ] CODE_OF_CONDUCT.md
- [ ] SECURITY.md

### Stage 10: DevOps
- [ ] Create Dockerfile
- [ ] Create docker-compose.yml
- [ ] Setup .github/workflows/ci.yml
- [ ] Test Docker build
- [ ] Verify all make commands work

### Stage 11: Testing and Validation
- [ ] Unit tests (DSL, renderer, statistics, acquisition)
- [ ] Integration tests (API consent/response/complete)
- [ ] E2E tests (full experiment flow)
- [ ] Security tests (no PII, admin protection)
- [ ] Run `make check` (lint + test + demo smoke)
- [ ] Fix all failures

### Stage 12: Final Report
- [ ] Create FINAL_REPORT.md
- [ ] Document what was done
- [ ] Document what was tested
- [ ] List commands that were run
- [ ] List limitations
- [ ] List what cannot be claimed
- [ ] Final commit

## Success Criteria
All criteria from Section 10 of the specification must be met:
1. pytest passes without network/GPU
2. ruff check passes
3. mypy passes (or limitations documented)
4. CLI demo creates 50+ PNGs and all artifacts
5. Web server runs and e2e test passes
6. Admin endpoints protected
7. No secrets, PII, or proprietary assets
8. README enables reproduction
9. All scientific claims honestly limited
10. All licenses and documentation present
11. Docker works (or limitation documented)
12. FINAL_REPORT.md complete
