# Ethical Considerations

## Overview

MirageForge is designed with ethical principles at its core. This document outlines the ethical framework, considerations, and requirements for using the platform in research.

## Core Ethical Principles

### 1. Respect for Persons
- **Informed Consent**: All participants must provide informed consent before participation
- **Voluntary Participation**: Participants can withdraw at any time without penalty
- **Age Requirement**: Participants must be 18 years or older
- **Autonomy**: Participants have full control over their participation

### 2. Beneficence
- **Minimize Harm**: No flashing, no fast motion, no photosensitive triggers
- **Maximize Benefits**: Contribute to understanding of visual perception
- **Risk Assessment**: Static visual stimuli pose minimal risk
- **Discomfort Warning**: Participants warned about potential visual discomfort

### 3. Justice
- **Fair Selection**: No discrimination in participant recruitment
- **Equal Treatment**: All participants receive same experience
- **Accessibility**: Platform designed for accessibility (keyboard navigation, ARIA labels)
- **No Exploitation**: No compensation that could be coercive

### 4. Privacy and Confidentiality
- **No PII Collection**: No IP addresses, user agents, names, emails, or addresses
- **Anonymous Sessions**: Only UUID tokens stored
- **Local Storage**: All data stored locally, no cloud uploads
- **No Tracking**: No analytics, no external services, no cookies beyond session

## Privacy by Design

### What We Don't Collect
- ✗ IP addresses
- ✗ User agents
- ✗ Names or identifiers
- ✗ Email addresses
- ✗ Phone numbers
- ✗ Physical addresses
- ✗ Age (beyond 18+ confirmation)
- ✗ Gender or demographics
- ✗ Location data
- ✗ Camera or microphone access

### What We Do Collect
- ✓ Anonymous session UUID
- ✓ Stimulus responses (choice, reaction time)
- ✓ Optional confidence ratings
- ✓ Timestamps (for analysis)

### Data Protection
- **Encryption**: Database can be encrypted at rest
- **Access Control**: Admin endpoints require token authentication
- **No External Transmission**: Data never leaves local system
- **Retention Policy**: Anonymous data retained for research; cannot be deleted individually

## Informed Consent Requirements

### Before Participation
Participants must be informed about:
1. **Purpose**: Research on visual perception
2. **Procedures**: Viewing static visual patterns, answering questions
3. **Duration**: Approximately 5-10 minutes
4. **Risks**: Potential mild visual discomfort
5. **Benefits**: Contribution to scientific knowledge
6. **Alternatives**: Can choose not to participate
7. **Confidentiality**: Anonymous data collection
8. **Contact**: Researcher contact information
9. **Voluntary**: Can stop at any time
10. **Questions**: Opportunity to ask questions

### Consent Process
1. Display comprehensive consent information
2. Require 18+ age confirmation
3. Require understanding confirmation
4. Require voluntary participation confirmation
5. Require explicit consent checkbox
6. Only then create session

### Consent Versioning
- Consent text version tracked with each session
- Allows tracking of consent changes over time
- Ensures reproducibility and auditability

## Risk Assessment

### Minimal Risk
Static visual stimuli are classified as minimal risk because:
- No physical contact
- No invasive procedures
- No sensitive personal information
- No deception (participants know it's perception research)
- No vulnerable populations (18+ only)

### Potential Risks
1. **Visual Discomfort**: Some patterns may cause mild discomfort
   - **Mitigation**: Warning in consent, stop button available
2. **Eye Strain**: Extended screen viewing
   - **Mitigation**: Short duration (5-10 min), breaks encouraged
3. **Boredom**: Repetitive task
   - **Mitigation**: Short experiment, interesting stimuli

### Risk Mitigation
- **Safety Validation**: All stimuli validated against photosensitivity guidelines
- **No Flashing**: Hard constraint - no flashing or flickering
- **No Fast Motion**: Hard constraint - only static images
- **Stop Button**: Always available during experiment
- **Debrief**: Explanation provided after completion
- **Contact**: Researcher contact for questions or concerns

## Vulnerable Populations

### Excluded Groups
The MVP explicitly excludes:
- **Children**: Under 18 years old
- **Cognitively Impaired**: Unable to provide informed consent
- **Visually Impaired**: May not be able to complete task
- **Photosensitive Epilepsy**: Risk from visual patterns
- **Prisoners**: Potential coercion
- **Employees/Students**: Potential coercion from authority

### Future Considerations
If including vulnerable populations:
- Additional ethical review required
- Modified consent procedures
- Additional safeguards
- Expert consultation required

## Data Management

### Collection
- Anonymous responses only
- No linking to individuals
- Timestamps for analysis
- Reaction times for research

### Storage
- Local database (SQLite/PostgreSQL)
- No cloud storage
- No external backup services
- Encrypted at rest (optional)

### Retention
- Anonymous data retained indefinitely for research
- Cannot delete individual responses (no identifiers)
- Participants informed of this limitation in consent

### Sharing
- Only aggregate, anonymized data shared
- No individual response data shared
- Data shared under appropriate license
- Compliance with data protection regulations

### Deletion
- Individual responses cannot be deleted (anonymous)
- Entire study can be deleted by administrator
- Participants informed of this limitation

## Ethical Approval Requirements

### For Real Research
Before conducting real experiments with human participants:

1. **IRB/Ethics Committee Approval**
   - Submit research protocol
   - Obtain approval before data collection
   - Follow institutional guidelines
   - Report any adverse events

2. **Institutional Oversight**
   - Affiliation with research institution
   - Faculty or PI supervision
   - Compliance with institutional policies

3. **Data Protection Compliance**
   - GDPR (Europe)
   - HIPAA (US, if applicable)
   - Local data protection laws
   - Institutional data governance

4. **Participant Protection**
   - Informed consent procedures
   - Debriefing procedures
   - Adverse event reporting
   - Participant withdrawal procedures

### For Demo/Synthetic Use
The synthetic demo does not require ethical approval because:
- No real participants involved
- No human data collected
- Clearly marked as synthetic
- For demonstration purposes only

## Responsible Use Guidelines

### For Researchers
1. **Obtain Ethical Approval**: Never skip IRB/ethics review
2. **Follow Protocol**: Adhere to approved research protocol
3. **Monitor Participants**: Watch for signs of discomfort
4. **Report Adverse Events**: Report any issues to IRB
5. **Maintain Privacy**: Protect participant anonymity
6. **Share Responsibly**: Only share anonymized, aggregate data
7. **Publish Honestly**: Report limitations and negative results
8. **Acknowledge Limitations**: Be transparent about platform limitations

### For Developers
1. **Test Thoroughly**: Ensure platform works correctly
2. **Document Limitations**: Be honest about what platform can/cannot do
3. **Security First**: Protect participant data
4. **Accessibility**: Design for diverse users
5. **No Dark Patterns**: Respect user autonomy
6. **Transparent Code**: Open source for transparency

### For Participants
1. **Read Consent**: Understand what you're agreeing to
2. **Ask Questions**: Clarify any uncertainties
3. **Stop if Uncomfortable**: Your wellbeing comes first
4. **Provide Honest Responses**: Help advance science
5. **Report Issues**: Let researchers know if problems occur

## Ethical Review Checklist

Before deploying for real research, verify:

- [ ] IRB/ethics approval obtained
- [ ] Informed consent procedures validated
- [ ] Participant protection measures in place
- [ ] Data protection compliance confirmed
- [ ] Risk assessment completed
- [ ] Adverse event reporting procedure established
- [ ] Participant withdrawal procedure tested
- [ ] Debriefing materials prepared
- [ ] Researcher contact information provided
- [ ] Data management plan approved
- [ ] Privacy policy reviewed
- [ ] Accessibility tested
- [ ] Security audit completed
- [ ] Documentation complete and accurate

## Conclusion

MirageForge is designed with strong ethical principles and privacy by design. However, **ethical design is not a substitute for ethical review**. Any real research using this platform must obtain appropriate ethical approval and follow institutional guidelines.

The synthetic demo allows testing and demonstration without ethical concerns, but real research requires real oversight.

---

**Remember**: Ethical research requires more than just ethical software. It requires ethical researchers, ethical institutions, and ethical oversight.
