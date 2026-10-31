# CLIPVisionBackend - Model Card

## Model Details
- **Name**: CLIP (Contrastive Language-Image Pre-training)
- **Version**: openai/clip-vit-base-patch32
- **Type**: Vision-language model
- **Status**: Optional (requires torch + transformers)

## Intended Use
- Comparing with human responses
- Identifying human-model divergence
- Research on visual perception
- **Not specifically trained on illusions**

## Training Data
Trained on 400 million image-text pairs from the internet (WIT dataset).

## Evaluation
Evaluated on various vision-language tasks. Not evaluated specifically on visual illusions.

## Limitations
- Not trained on illusions
- Image-text similarity may not match human perception
- May not capture perceptual effects
- Requires significant compute (GPU recommended)
- Optional dependency

## Ethical Considerations
- Trained on internet data (potential biases)
- May reflect societal biases
- Use with awareness of limitations

## References
Radford et al. (2021). Learning Transferable Visual Models From Natural Language Supervision. ICML.
TODO: Verify reference and add DOI.
