# MirageForge Assumptions

This document lists all assumptions made during the implementation of MirageForge MVP where requirements were ambiguous or data was unavailable.

## Technical Assumptions

### 1. Python Environment
- **Assumption**: Python 3.11+ is available on the target system
- **Rationale**: Specified in requirements; modern Python features (type hints, pattern matching) are beneficial
- **Impact**: None; this is a hard requirement

### 2. Database Backend
- **Assumption**: SQLite is used by default for local development and demo; PostgreSQL is optional for production
- **Rationale**: SQLite requires no setup, perfect for demo and tests; PostgreSQL provides scalability for real deployments
- **Impact**: DATABASE_URL environment variable allows switching; code uses SQLAlchemy ORM for portability

### 3. Stimulus Rendering
- **Assumption**: All stimuli are rendered at 1024x1024 pixels unless specified otherwise in stimulus spec
- **Rationale**: High enough resolution for web display and analysis; not too large for storage
- **Impact**: Consistent stimulus quality; file sizes ~50-200KB per PNG

### 4. Color Space
- **Assumption**: sRGB color space is used for all stimuli
- **Rationale**: Standard for web displays; most monitors approximate sRGB
- **Impact**: Color perception experiments assume sRGB-capable displays; this is documented in limitations

### 5. Random Number Generation
- **Assumption**: numpy.random.default_rng(seed) is used for all random operations
- **Rationale**: Modern numpy RNG with reproducible seeding; better than legacy numpy.random
- **Impact**: Deterministic results when seed is fixed; required for reproducibility

### 6. Vision Model Mock Scores
- **Assumption**: MockVisionModel returns pseudo-scores based on stimulus SHA256 hash
- **Rationale**: Deterministic, reproducible, clearly marked as mock; no network/GPU required
- **Impact**: Scores are stable but not meaningful; clearly labeled as mock in all outputs

### 7. Simulated Human Model
- **Assumption**: SimulatedHumanModel uses parameterized psychometric functions with noise
- **Rationale**: Simulates realistic human response patterns without real participants
- **Impact**: Synthetic data follows expected patterns but is not real human data; marked SYNTHETIC

### 8. Active Search Parameters
- **Assumption**: Default search uses 200 candidates, 3 rounds, selects top 12 stimuli
- **Rationale**: Reasonable for demo; fast enough (<5 min on CPU); shows algorithm behavior
- **Impact**: Demonstrates search capability; not sufficient for real research (documented)

### 9. Web Experiment Trials
- **Assumption**: Default experiment has 12-15 trials per session
- **Rationale**: Short enough to prevent fatigue; long enough to gather meaningful data
- **Impact**: Configurable via Study.config JSON; can be adjusted for real studies

### 10. Reaction Time Measurement
- **Assumption**: Reaction time is measured client-side from stimulus display to response submission
- **Rationale**: Server-side measurement includes network latency; client-side is more accurate for perception tasks
- **Impact**: Requires JavaScript; documented in protocol; may have small measurement error

### 11. Consent and Age Verification
- **Assumption**: Self-reported 18+ checkbox is sufficient for MVP
- **Rationale**: No PII collected; cannot verify age without collecting personal data
- **Impact**: Relies on user honesty; real study would need proper age verification (documented)

### 12. Data Retention
- **Assumption**: Anonymous responses are retained indefinitely for research purposes
- **Rationale**: Cannot link responses to individuals for deletion; standard practice for anonymous surveys
- **Impact**: Documented in consent and privacy policy; users informed before participation

### 13. Rate Limiting
- **Assumption**: In-memory rate limiting per session token (100 requests/minute)
- **Rationale**: Prevents abuse without storing IP addresses; sufficient for MVP
- **Impact**: Rate limit resets on server restart; production should use Redis or similar

### 14. Admin Token
- **Assumption**: ADMIN_TOKEN is a simple string comparison; no JWT or OAuth
- **Rationale**: MVP simplicity; admin endpoints are optional and disabled by default
- **Impact**: Secure if token is strong and HTTPS is used; production should use proper auth

### 15. CLIP Backend
- **Assumption**: CLIP uses openai/clip-vit-base-patch32 model if available
- **Rationale**: Lightweight, CPU-friendly, well-documented; graceful fallback if unavailable
- **Impact**: Optional dependency; tests and demo work without it; clearly marked as optional

### 16. Statistical Significance
- **Assumption**: p < 0.05 after Benjamini-Hochberg correction is considered significant
- **Rationale**: Standard threshold in psychology research; BH correction for multiple comparisons
- **Impact**: Conservative approach; may miss real effects with small samples (documented)

### 17. Bootstrap Samples
- **Assumption**: 1000 bootstrap samples for confidence intervals
- **Rationale**: Standard practice; balances accuracy and computation time
- **Impact**: CI width may vary; 10000 samples would be more precise but slower

### 18. Jensen-Shannon Divergence
- **Assumption**: JSD is calculated with base-2 logarithm (bits)
- **Rationale**: Standard information-theoretic measure; interpretable as bits of divergence
- **Impact**: Values in [0, 1] bits; consistent with literature

## Scientific Assumptions

### 19. Illusion Families
- **Assumption**: 5 stimulus families are sufficient to demonstrate platform capability
- **Rationale**: Covers major illusion categories (size, geometry, contrast, crowding, detection)
- **Impact**: Demonstrates versatility; real research would need more families and variations

### 20. Divergence Metric
- **Assumption**: Absolute difference in choice proportions + JSD captures human-model divergence
- **Rationale**: Simple, interpretable, covers both magnitude and distribution shape
- **Impact**: May miss subtler divergences; sufficient for MVP; can be extended

### 21. Candidate Selection
- **Assumption**: Stimuli with highest predicted divergence are most interesting candidates
- **Rationale**: Efficient search strategy; focuses on where models fail
- **Impact**: May miss other interesting stimuli (e.g., high agreement); documented as limitation

### 22. Synthetic Validation
- **Assumption**: Synthetic demo validates software correctness, not scientific claims
- **Rationale**: No real participants; cannot validate illusions without human data
- **Impact**: Clearly marked SYNTHETIC; no claims about actual illusions (documented everywhere)

## Ethical Assumptions

### 23. Risk Assessment
- **Assumption**: Static visual stimuli pose minimal risk to participants
- **Rationale**: No flashing, no disturbing content, no PII collection
- **Impact**: Minimal risk study; still requires IRB approval for real research (documented)

### 24. Visual Discomfort
- **Assumption**: Some participants may experience mild visual discomfort from certain patterns
- **Rationale**: Known effect for high-contrast patterns, gratings, crowding stimuli
- **Impact**: Warning in consent; stop button available; documented in protocol

### 25. Accessibility
- **Assumption**: Colorblind-friendly palettes and keyboard navigation are sufficient for MVP
- **Rationale**: Basic accessibility without requiring specialized equipment
- **Impact**: Some visual impairments may prevent participation; documented in accessibility.md

### 26. Data Anonymity
- **Assumption**: UUID session tokens with no IP/user-agent storage provide sufficient anonymity
- **Rationale**: Cannot link responses to individuals; standard practice
- **Impact**: Cannot delete individual responses after submission; documented in consent

## Operational Assumptions

### 27. Network Availability
- **Assumption**: Network is available only for pip install and optional model download
- **Rationale**: Core functionality must work offline; tests and demo require no network
- **Impact**: CLIP backend gracefully degrades; mock backends always available

### 28. GPU Availability
- **Assumption**: No GPU is available or required
- **Rationale**: All components work on CPU; CLIP is optional and CPU-friendly
- **Impact**: Slower inference if CLIP is used; acceptable for MVP; documented

### 29. Docker Availability
- **Assumption**: Docker is available on developer machines but may not be available in all environments
- **Rationale**: Docker is standard for deployment but not required for development
- **Impact**: docker-compose.yml provided; if Docker unavailable, documented in FINAL_REPORT.md

### 30. Continuous Integration
- **Assumption**: GitHub Actions is available for CI
- **Rationale**: Standard for GitHub repositories; free for public repos
- **Impact**: .github/workflows/ci.yml provided; if unavailable, tests can be run locally

## Documentation Assumptions

### 31. Citation Format
- **Assumption**: CITATION.cff uses placeholder values (author, DOI, etc.)
- **Rationale**: Real citation metadata requires publication; placeholders allow future updates
- **Impact**: Users must update with real metadata before publication

### 32. Model Cards
- **Assumption**: Model cards follow Hugging Face format and guidelines
- **Rationale**: Industry standard; familiar to ML practitioners
- **Impact**: Consistent documentation; can be extended for real models

### 33. Datasheet
- **Assumption**: Datasheet follows "Datasheets for Datasets" framework
- **Rationale**: Standard for dataset documentation; promotes transparency
- **Impact**: Comprehensive documentation; may need updates for real data

## Future Work Assumptions

### 34. Real Human Studies
- **Assumption**: This MVP is a platform demonstration, not a real study
- **Rationale**: No IRB approval, no real participants, no validated illusions
- **Impact**: All results marked SYNTHETIC; real study requires ethics approval, recruitment, validation

### 35. Model Improvements
- **Assumption**: MockVisionModel and SimulatedHumanModel are placeholders
- **Rationale**: Demonstrate interface; real models require training, validation, compute
- **Impact**: Clearly marked as mock/synthetic; can be replaced with real models later

### 36. Stimulus Families
- **Assumption**: 5 families demonstrate capability; more families can be added
- **Rationale**: Extensible architecture; new families follow same DSL pattern
- **Impact**: Platform can grow; initial release focuses on core functionality

## Assumptions About User Intent

### 37. Portfolio Project
- **Assumption**: This is a portfolio/demonstration project, not a production research platform
- **Rationale**: User specified "personal portfolio project"; no MIT affiliation claims
- **Impact**: Focus on code quality, documentation, reproducibility; not on scale or performance

### 38. Learning Goals
- **Assumption**: Project demonstrates full-stack ML engineering, research methodology, and ethical AI
- **Rationale**: Covers multiple domains: backend, frontend, ML, statistics, ethics, documentation
- **Impact**: Comprehensive implementation; showcases diverse skills

### 39. Open Source
- **Assumption**: Project will be publicly available under MIT license
- **Rationale**: User specified MIT license; open research promotes transparency
- **Impact**: Code and documentation must be clear, reproducible, and welcoming to contributors

---

## Revision History

- **2026-10-31**: Initial assumptions document created during project planning phase
- Assumptions will be updated as implementation reveals new constraints or decisions
