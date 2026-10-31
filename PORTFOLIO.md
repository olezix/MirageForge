# MirageForge - Portfolio Summary

## Project Overview

**MirageForge** is an open research platform for AI-driven discovery of candidate visual illusions and measuring divergence between human perception and vision models.

### The Problem

Understanding human visual perception requires:
1. Identifying stimuli that produce interesting perceptual effects
2. Comparing human responses with computational models
3. Finding where models fail to match human perception

Traditional approaches are manual, time-consuming, and limited by human intuition. Can AI help search the vast space of visual stimuli to find candidates worth studying?

### The Idea

MirageForge uses active learning to:
- Generate parameterized visual stimuli across multiple families
- Run experiments with humans (or synthetic simulators for testing)
- Compare human responses with vision model predictions
- Identify stimuli that maximize human-model divergence
- Prioritize candidates for real validation

### What Makes This Different

Unlike typical AI applications that use models as end products, MirageForge uses AI as a **research tool**:
- AI generates and evaluates candidates
- AI identifies interesting regions of stimulus space
- Humans validate findings through real experiments
- Platform supports the full research workflow

## Technical Architecture

### Stimulus Generation
- **DSL**: Pydantic v2 schemas for 5 stimulus families
- **Renderer**: Pillow + NumPy for deterministic PNG generation
- **Safety**: Validation against photosensitivity guidelines
- **Reproducibility**: SHA256 checksums, fixed seeds

### Vision Backends
- **MockVisionModel**: Deterministic pseudo-scores for testing
- **SimulatedHumanModel**: Synthetic responses with psychometric functions
- **CLIPVisionBackend**: Optional real model (graceful fallback)

### Active Search
- **Candidate Generation**: Random sampling + parameter mutations
- **Acquisition Strategies**: UCB, random, diversity-based
- **Divergence Metrics**: Jensen-Shannon, absolute difference
- **Archive**: Track candidates, scores, and history

### Web Platform
- **FastAPI**: Modern async web framework
- **Consent Flow**: 18+ verification, informed consent
- **Experiment Interface**: Trial presentation, response recording
- **Privacy**: Anonymous sessions, no PII, no tracking

### Statistical Analysis
- **Confidence Intervals**: Wilson, bootstrap
- **Divergence**: Jensen-Shannon, absolute difference
- **Multiple Comparisons**: Benjamini-Hochberg correction
- **Export**: CSV, JSON, Markdown reports

## How AI Was Used as a Research Tool

### AI for Generation
- Parameterized stimulus families
- Systematic exploration of stimulus space
- Mutation operators for local search

### AI for Evaluation
- Vision models predict responses
- Divergence metrics identify interesting stimuli
- Acquisition strategies balance exploration/exploitation

### AI for Analysis
- Automated statistical analysis
- Report generation
- Candidate ranking

### Human Validation (Future)
- Real participants provide ground truth
- Controlled experiments validate candidates
- Peer review ensures scientific rigor

## What Was Validated

### Software Validation ✓
- Stimulus rendering is deterministic and reproducible
- Database operations work correctly
- CLI commands execute successfully
- Web interface is functional
- Statistics are calculated correctly

### Pipeline Validation ✓
- Full demo pipeline runs end-to-end
- Generates 50+ stimuli
- Runs synthetic experiments
- Produces reports and galleries

### What Was NOT Validated
- ✗ Real human perception (by design - demo only)
- ✗ Scientific claims about illusions
- ✗ Platform effectiveness for research
- ✗ Generalizability to human vision

## Synthetic Results

All demo results are explicitly marked **SYNTHETIC**:
- Human responses from SimulatedHumanModel
- Divergence scores from synthetic comparisons
- Candidate selections from synthetic evaluation
- Statistical analysis of synthetic data

**These are not real research results.**

## Limitations

### Technical
- Small demo scale (~200 candidates)
- Simplified psychometric models
- Limited stimulus families (5)
- CPU-only processing

### Scientific
- No real human validation
- No ethical approval
- No peer review
- No statistical power analysis

### Ethical
- Platform not validated for real research
- Requires IRB approval before use
- Cannot replace controlled lab studies

## How to Reproduce the Demo

```bash
git clone https://github.com/mirageforge/mirageforge.git
cd mirageforge
pip install -e ".[dev]"
make init-db
make demo
```

This generates:
- 50+ PNG stimuli in `artifacts/demo/stimuli/`
- Interactive gallery at `artifacts/demo/index.html`
- Analysis report at `artifacts/demo/report.md`
- Statistics at `artifacts/demo/metrics.json`

All outputs marked SYNTHETIC.

## Next Steps for Real Research

1. **Obtain Ethical Approval**
   - Submit to IRB/ethics committee
   - Get approval before data collection

2. **Recruit Real Participants**
   - 18+ adults with informed consent
   - Appropriate sample size (power analysis)
   - Diverse demographics

3. **Conduct Controlled Experiments**
   - Calibrated displays
   - Standardized protocols
   - Quality control measures

4. **Validate Findings**
   - Replicate with independent samples
   - Compare with literature
   - Peer review results

5. **Publish and Share**
   - Open methodology
   - Share data (anonymized)
   - Contribute to scientific knowledge

## What I Built vs. What AI Helped With

### I Designed
- Overall architecture and workflow
- Stimulus families and parameters
- Statistical methodology
- Privacy and ethical framework
- Documentation structure

### AI Assisted With
- Implementation of specific functions
- Code review and suggestions
- Documentation drafting
- Test case generation
- Debugging and optimization

### I Validated
- All code runs correctly
- Tests pass
- Demo produces expected outputs
- Documentation is accurate
- Limitations are honestly stated

## Key Takeaways

1. **AI as Tool, Not Replacement**: AI helps search stimulus space, but humans validate findings
2. **Reproducibility Matters**: Deterministic rendering, fixed seeds, checksums
3. **Privacy by Design**: No PII, anonymous sessions, local storage
4. **Honest Limitations**: Clear about what is/isn't validated
5. **Ethical Responsibility**: Requires IRB approval for real research
6. **Open Science**: Code, data, and methodology are open

## Technologies Used

- **Python 3.11+**: Core language
- **FastAPI**: Web framework
- **SQLAlchemy 2.0**: Database ORM
- **Pydantic v2**: Data validation
- **Pillow + NumPy**: Image rendering
- **SciPy**: Statistical analysis
- **Ruff + Mypy**: Code quality
- **Pytest**: Testing
- **Docker**: Containerization

## Skills Demonstrated

- **Full-Stack Development**: Backend, frontend, database, CLI
- **ML Engineering**: Vision models, active learning, evaluation
- **Research Methodology**: Experimental design, statistics, validation
- **Ethics and Privacy**: Privacy by design, informed consent, IRB
- **Documentation**: Technical writing, reproducibility, transparency
- **Software Engineering**: Testing, CI/CD, containerization

## Conclusion

MirageForge demonstrates a complete platform for AI-assisted visual perception research. While all demo results are synthetic, the platform provides a solid foundation for real research with proper validation and ethical oversight.

The project showcases:
- Technical implementation skills
- Understanding of research methodology
- Commitment to ethical AI
- Transparency about limitations
- Reproducibility and open science

**Status**: MVP Complete - Ready for Real Validation  
**Code**: Open source under MIT license  
**Data**: All synthetic, clearly marked  
**Validation**: Software tested, science not validated

---

*This portfolio summary honestly represents what was built, what was tested, and what remains to be done.*
