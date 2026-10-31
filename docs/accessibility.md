# Accessibility

## Overview

MirageForge is designed with accessibility in mind. This document describes accessibility features and limitations.

## Accessibility Features

### Keyboard Navigation
- All interactive elements accessible via keyboard
- Tab navigation between elements
- Enter/Space to activate buttons
- Arrow keys for option selection (where applicable)
- Escape to stop experiment

### Screen Reader Support
- Semantic HTML structure
- ARIA labels for interactive elements
- Alt text for images
- Clear heading hierarchy
- Form labels properly associated

### Visual Design
- High contrast text (WCAG AA compliant)
- Clear focus indicators
- Sufficient color contrast
- Readable font sizes
- Consistent layout

### Cognitive Accessibility
- Clear, simple language
- Consistent navigation
- Progress indicators
- Ability to stop at any time
- No time pressure

### Motor Accessibility
- Large click targets
- Keyboard alternatives for all actions
- No precise timing requirements
- No dragging or complex gestures

## Limitations

### Visual Task Requirements
- Requires ability to see visual stimuli
- No alternative modalities (audio, tactile)
- May not be suitable for visually impaired users
- Color perception may affect some tasks

### Browser Compatibility
- Modern browsers required
- JavaScript required
- May not work with very old assistive technologies

### Known Issues
- Some visual illusions may be less effective with certain visual impairments
- Reaction time measurements may be affected by assistive technology
- Touch screen support limited

## Testing

### Tested With
- Keyboard-only navigation
- Screen readers (basic testing)
- High contrast modes
- Different screen sizes

### Not Tested With
- Eye tracking devices
- Switch access devices
- Voice control software
- All assistive technologies

## Recommendations for Improvement

### For Researchers
1. Provide alternative text descriptions of stimuli
2. Allow extended time for responses
3. Provide practice trials
4. Offer breaks between blocks
5. Consider multiple modalities in future versions

### For Developers
1. Test with diverse assistive technologies
2. Follow WCAG 2.1 AA guidelines
3. Conduct user testing with disabled users
4. Provide accessibility statement
5. Create feedback mechanism for accessibility issues

## Compliance

### Standards
- WCAG 2.1 Level AA (partial compliance)
- Section 508 (basic compliance)
- EN 301 549 (basic compliance)

### Not Compliant With
- WCAG 2.1 Level AAA
- Full Section 508 compliance
- All EN 301 549 requirements

## Contact

For accessibility issues or suggestions:
- Open GitHub issue with "accessibility" label
- Contact research team
- Provide specific details about the issue

## Future Improvements

Planned improvements:
- Audio descriptions of stimuli
- Haptic feedback options
- More comprehensive screen reader testing
- User testing with disabled participants
- Alternative response methods

---

**Last Updated**: 2026-10-31  
**Version**: 1.0.0
