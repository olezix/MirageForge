# Limitations

## Overview

This document provides a comprehensive list of limitations for the MirageForge platform. Understanding these limitations is crucial for responsible use and accurate interpretation of results.

## Technical Limitations

### Stimulus Generation
1. **Limited Families**: Only 5 stimulus families implemented
   - Size context (Ebbinghaus-like)
   - Line context (Müller-Lyer-like)
   - Contrast
   - Crowding
   - Grating
   - Many other illusion types not supported

2. **Simplified Parameters**: Parameter ranges may not cover all interesting stimuli
   - Conservative safety bounds
   - May miss extreme but interesting cases
   - Requires manual tuning for specific research questions

3. **Static Only**: No dynamic or animated stimuli
   - No motion illusions
   - No temporal effects
   - No adaptation paradigms

4. **2D Only**: No 3D or stereoscopic stimuli
   - No depth perception illusions
   - No binocular rivalry
   - Limited to monocular viewing

5. **Color Space**: Assumes sRGB
   - May not match all displays
   - No color calibration
   - Limited color gamut

### Rendering
1. **Resolution**: Fixed at 1024x1024 or smaller
   - May not be optimal for all displays
   - No high-DPI support
   - Limited detail for fine patterns

2. **No Anti-aliasing**: Simple rendering without advanced techniques
   - May produce jagged edges
   - Limited visual quality

3. **Deterministic but Simplified**: Same seed → same image, but rendering is simplified
   - Not photorealistic
   - May not match laboratory stimuli quality

### Vision Models
1. **MockVisionModel**: Not a real vision model
   - Pseudo-random predictions
   - No actual visual processing
   - For testing only

2. **SimulatedHumanModel**: Simplified psychometric functions
   - Based on literature, not real data
   - May not capture real human variability
   - Synthetic responses only

3. **CLIP Backend**: Not trained on illusions
   - General vision-language model
   - May not capture perceptual effects
   - Image-text similarity ≠ human perception

4. **No Training**: Models are not trained on experimental data
   - No fine-tuning on human responses
   - No adaptation to specific tasks
   - Generic predictions only

### Active Search
1. **Small Scale**: Default demo uses ~200 candidates
   - Real research may need thousands
   - Limited exploration of stimulus space
   - May miss global optima

2. **Simple Acquisition**: UCB and random strategies only
   - No advanced Bayesian optimization
   - No multi-objective optimization
   - Limited exploration-exploitation balance

3. **Simplified Divergence**: Basic metrics only
   - Jensen-Shannon divergence
   - Absolute difference
   - May not capture all interesting divergences

4. **No Constraints**: Limited constraint handling
   - May generate invalid or unsafe stimuli
   - Requires manual validation
   - No automatic safety checking beyond basic rules

### Web Platform
1. **No Display Calibration**: Assumes standard displays
   - No color calibration
   - No luminance calibration
   - No viewing distance control

2. **Uncontrolled Environment**: Participants' environments vary
   - Different lighting conditions
   - Different screen sizes
   - Different viewing distances
   - Distractions possible

3. **No Eye Tracking**: Cannot verify fixation or attention
   - Participants may not look at stimuli
   - No gaze data
   - No attention monitoring

4. **Client-Side Timing**: Reaction times measured client-side
   - Network latency not accounted for
   - Browser variability
   - Less accurate than laboratory equipment

5. **No Quality Control**: Limited participant quality checks
   - No attention checks
   - No catch trials
   - No performance monitoring

### Statistical Analysis
1. **Basic Methods**: Standard statistical tests only
   - Wilson CI, bootstrap, chi-squared
   - No advanced hierarchical models
   - No Bayesian analysis
   - No mixed-effects models

2. **Small Samples**: Demo has limited statistical power
   - Default 12 trials per session
   - May not detect small effects
   - Wide confidence intervals

3. **Multiple Comparisons**: BH correction only
   - Conservative approach
   - May miss real effects
   - No FDR estimation

4. **No Power Analysis**: No automatic sample size calculation
   - Users must determine appropriate sample size
   - Risk of underpowered studies

### Database
1. **SQLite Default**: Not suitable for production
   - Single-user limitations
   - No concurrent writes
   - Limited scalability

2. **No Backup**: No automatic backup system
   - Risk of data loss
   - Manual backup required

3. **No Encryption**: Database not encrypted by default
   - Security risk if compromised
   - Requires manual encryption setup

## Scientific Limitations

### Validation
1. **No Real Validation**: All demo results are synthetic
   - No real human participants
   - No ground truth
   - Cannot validate platform effectiveness

2. **No Replication**: No independent replication
   - Single implementation
   - No cross-validation
   - No external verification

3. **No Peer Review**: Platform not reviewed by domain experts
   - No vision scientist review
   - No statistical review
   - No ethical review

4. **No Benchmarking**: No comparison with existing methods
   - Unknown relative performance
   - No baseline comparisons
   - No standard datasets

### Generalizability
1. **Online vs Laboratory**: Web experiments differ from lab studies
   - Less control
   - More variability
   - Different participant populations
   - Different motivation levels

2. **Sample Bias**: Self-selected participants
   - Not representative of general population
   - May have specific interests
   - Limited demographic diversity

3. **Cultural Factors**: Illusions may vary across cultures
   - No cultural validation
   - Western-centric design
   - Limited cross-cultural applicability

4. **Individual Differences**: Large variability in perception
   - Age effects not studied
   - Visual acuity not measured
   - No individual difference analysis

### Interpretation
1. **Correlation ≠ Causation**: Platform identifies candidates, not causes
   - Cannot explain why illusions occur
   - No mechanistic understanding
   - Requires further research

2. **Candidates ≠ Illusions**: Selected stimuli are candidates, not validated illusions
   - Require independent validation
   - May not produce reliable effects
   - May be artifacts of procedure

3. **Synthetic ≠ Real**: Synthetic results do not predict real results
   - Simulated humans ≠ real humans
   - Mock models ≠ real models
   - Demo results are illustrative only

4. **No Causal Claims**: Platform cannot make causal claims
   - Observational only
   - No experimental manipulation
   - No causal inference

## Ethical Limitations

### Consent
1. **Self-Reported Age**: Age verification is self-reported
   - Cannot verify actual age
   - Children could participate
   - Relies on honesty

2. **Online Consent**: May not be as thorough as in-person
   - Participants may not read carefully
   - No opportunity for questions
   - Limited comprehension checking

3. **No Comprehension Check**: Cannot verify understanding
   - Participants may not understand
   - No quiz or verification
   - Relies on self-assessment

### Privacy
1. **Cannot Delete Individual Data**: Anonymous data cannot be deleted
   - No way to identify individual responses
   - Participants cannot withdraw data
   - Must inform participants of this limitation

2. **No Anonymity Guarantee**: Cannot guarantee complete anonymity
   - Browser fingerprinting possible
   - Network metadata may exist
   - Theoretical re-identification risk

3. **Local Storage Only**: No secure cloud backup
   - Risk of data loss
   - Limited disaster recovery
   - Manual backup required

### Accessibility
1. **Visual Task Only**: Requires normal or corrected vision
   - Excludes visually impaired
   - No alternative modalities
   - Limited accessibility

2. **Keyboard Only**: Limited input methods
   - No touch gestures
   - No voice commands
   - May exclude some users

3. **Language**: English only
   - No multilingual support
   - Excludes non-English speakers
   - Cultural bias

## Operational Limitations

### Performance
1. **CPU Only**: No GPU acceleration
   - Slow rendering for large batches
   - Slow model inference
   - Limited scalability

2. **Memory**: Loads all candidates into memory
   - Limited by RAM
   - Cannot handle very large searches
   - No streaming or batching

3. **Single Thread**: Limited parallelization
   - Sequential processing
   - Slow for large experiments
   - No distributed computing

### Reliability
1. **No Monitoring**: No system health monitoring
   - No alerting
   - No automatic recovery
   - Manual intervention required

2. **No Load Testing**: Unknown performance under load
   - May fail with many concurrent users
   - No stress testing
   - Unknown limits

3. **No Error Recovery**: Limited error handling
   - May lose data on crashes
   - No automatic retry
   - Manual recovery required

### Maintenance
1. **No Updates**: No automatic update mechanism
   - Manual updates required
   - Risk of running outdated versions
   - No version management

2. **No Monitoring**: No usage analytics
   - Cannot track adoption
   - Cannot identify issues
   - Limited feedback

3. **Documentation**: Documentation may be incomplete
   - Some features undocumented
   - Examples may be missing
   - May become outdated

## What Cannot Be Claimed

Based on this platform and demo results, we **CANNOT** claim:

1. ✗ That new illusions have been discovered
2. ✗ That specific stimuli cause specific perceptual effects
3. ✗ That the platform is validated for research use
4. ✗ That AI can replace human perception studies
5. ✗ That the platform is "first" or "breakthrough"
6. ✗ Any medical or diagnostic conclusions
7. ✗ That results generalize to all populations
8. ✗ That the platform is production-ready
9. ✗ That synthetic results predict real results
10. ✗ That the platform is superior to existing methods

## Responsible Use Guidelines

### Before Using for Real Research
1. **Obtain Ethical Approval**: Never skip IRB/ethics review
2. **Validate Platform**: Test thoroughly with pilot studies
3. **Consult Experts**: Work with vision scientists and statisticians
4. **Understand Limitations**: Read and understand all limitations
5. **Plan Appropriately**: Design studies with limitations in mind
6. **Report Honestly**: Be transparent about limitations in publications
7. **Validate Findings**: Replicate with independent methods
8. **Peer Review**: Submit to peer-reviewed venues

### When Interpreting Results
1. **Check Sample Size**: Ensure adequate statistical power
2. **Consider Variability**: Account for individual differences
3. **Question Assumptions**: Verify platform assumptions
4. **Seek Replication**: Replicate findings independently
5. **Consult Literature**: Compare with existing research
6. **Be Conservative**: Avoid overclaiming results
7. **Acknowledge Limits**: Explicitly state limitations
8. **Suggest Future Work**: Identify what remains to be done

## Conclusion

MirageForge is a research platform with significant limitations. It is designed to **generate candidates** for further study, not to provide definitive answers about visual perception.

**Key Takeaways**:
- All demo results are SYNTHETIC
- Platform requires real validation before research use
- Results are candidates, not validated illusions
- Ethical approval required for real research
- Limitations must be acknowledged in any publication

Use this platform responsibly, understand its limitations, and never overclaim results.

---

**Remember**: A tool's limitations are not weaknesses if they are understood and acknowledged. They are boundaries that define appropriate use.
