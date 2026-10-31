"""
Statistical analysis for experiment results.

Provides functions for calculating confidence intervals, divergence metrics,
and statistical significance tests.
"""

from typing import Any

import numpy as np
from scipy import stats


def wilson_ci_proportion(
    successes: int,
    total: int,
    confidence: float = 0.95,
) -> tuple[float, float, float]:
    """
    Calculate Wilson confidence interval for a proportion.

    Args:
        successes: Number of successes
        total: Total number of trials
        confidence: Confidence level (default 0.95)

    Returns:
        Tuple of (proportion, lower_bound, upper_bound)
    """
    if total == 0:
        return (0.0, 0.0, 0.0)

    proportion = successes / total
    z = stats.norm.ppf(1 - (1 - confidence) / 2)

    denominator = 1 + z**2 / total
    center = (proportion + z**2 / (2 * total)) / denominator
    spread = z * np.sqrt((proportion * (1 - proportion) + z**2 / (4 * total)) / total) / denominator

    lower = max(0.0, center - spread)
    upper = min(1.0, center + spread)

    return (proportion, lower, upper)


def bootstrap_ci_difference(
    human_responses: np.ndarray,
    model_responses: np.ndarray,
    num_samples: int = 1000,
    confidence: float = 0.95,
    seed: int = 42,
) -> tuple[float, float, float]:
    """
    Calculate bootstrap confidence interval for difference in means.

    Args:
        human_responses: Array of human responses (0/1 or probabilities)
        model_responses: Array of model responses
        num_samples: Number of bootstrap samples
        confidence: Confidence level
        seed: Random seed

    Returns:
        Tuple of (mean_difference, lower_bound, upper_bound)
    """
    rng = np.random.default_rng(seed)

    if len(human_responses) == 0 or len(model_responses) == 0:
        return (0.0, 0.0, 0.0)

    # Observed difference
    observed_diff = np.mean(human_responses) - np.mean(model_responses)

    # Bootstrap samples
    bootstrap_diffs = []
    for _ in range(num_samples):
        h_sample = rng.choice(human_responses, size=len(human_responses), replace=True)
        m_sample = rng.choice(model_responses, size=len(model_responses), replace=True)
        bootstrap_diffs.append(np.mean(h_sample) - np.mean(m_sample))

    bootstrap_diffs = np.array(bootstrap_diffs)

    # Calculate CI
    alpha = 1 - confidence
    lower = np.percentile(bootstrap_diffs, 100 * alpha / 2)
    upper = np.percentile(bootstrap_diffs, 100 * (1 - alpha / 2))

    return (observed_diff, lower, upper)


def jensen_shannon_divergence(
    p: np.ndarray,
    q: np.ndarray,
    base: float = 2.0,
) -> float:
    """
    Calculate Jensen-Shannon divergence between two distributions.

    JSD is a symmetric, bounded measure of divergence.

    Args:
        p: First probability distribution
        q: Second probability distribution
        base: Logarithm base (default 2 for bits)

    Returns:
        JSD value in [0, 1] (for base 2)
    """
    # Normalize
    p = np.asarray(p)
    q = np.asarray(q)
    p = p / p.sum()
    q = q / q.sum()

    # Calculate midpoint
    m = 0.5 * (p + q)

    # Calculate KL divergences
    def kl_div(a: np.ndarray, b: np.ndarray) -> float:
        """KL divergence with protection against log(0)."""
        mask = a > 0
        return float(np.sum(a[mask] * np.log(a[mask] / b[mask]) / np.log(base)))

    kl_pm = kl_div(p, m)
    kl_qm = kl_div(q, m)

    jsd = 0.5 * (kl_pm + kl_qm)

    return min(1.0, max(0.0, jsd))


def absolute_difference(
    human_dist: np.ndarray,
    model_dist: np.ndarray,
) -> float:
    """
    Calculate absolute difference between two distributions.

    Args:
        human_dist: Human response distribution
        model_dist: Model response distribution

    Returns:
        Mean absolute difference
    """
    human_dist = np.asarray(human_dist)
    model_dist = np.asarray(model_dist)

    # Normalize
    human_dist = human_dist / human_dist.sum()
    model_dist = model_dist / model_dist.sum()

    return float(np.mean(np.abs(human_dist - model_dist)))


def benjamini_hochberg(
    p_values: list[float],
    alpha: float = 0.05,
) -> list[tuple[float, bool]]:
    """
    Apply Benjamini-Hochberg correction for multiple comparisons.

    Controls false discovery rate (FDR).

    Args:
        p_values: List of p-values
        alpha: Significance level

    Returns:
        List of (p_value, is_significant) tuples
    """
    if not p_values:
        return []

    n = len(p_values)

    # Sort p-values with original indices
    sorted_pvals = sorted(enumerate(p_values), key=lambda x: x[1])

    # Calculate BH thresholds
    [alpha * (i + 1) / n for i in range(n)]

    # Find largest k where p(k) <= threshold(k)
    significant_indices = set()
    for i, (_idx, pval) in enumerate(reversed(sorted_pvals)):
        k = n - i
        threshold = alpha * k / n
        if pval <= threshold:
            # All p-values up to this one are significant
            for j in range(n - i):
                significant_indices.add(sorted_pvals[j][0])
            break

    # Build result
    results = []
    for i, pval in enumerate(p_values):
        results.append((pval, i in significant_indices))

    return results


def chi_squared_test(
    observed: np.ndarray,
    expected: np.ndarray,
) -> tuple[float, float]:
    """
    Perform chi-squared test for goodness of fit.

    Args:
        observed: Observed frequencies
        expected: Expected frequencies

    Returns:
        Tuple of (chi2_statistic, p_value)
    """
    observed = np.asarray(observed)
    expected = np.asarray(expected)

    # Normalize expected to match observed total
    expected = expected * (observed.sum() / expected.sum())

    # Avoid division by zero
    mask = expected > 0
    if not mask.any():
        return (0.0, 1.0)

    chi2 = np.sum((observed[mask] - expected[mask]) ** 2 / expected[mask])
    df = mask.sum() - 1

    if df <= 0:
        return (chi2, 1.0)

    p_value = 1 - stats.chi2.cdf(chi2, df)

    return (float(chi2), float(p_value))


def calculate_divergence_metrics(
    human_responses: dict[str, int],
    model_predictions: dict[str, float],
) -> dict[str, Any]:
    """
    Calculate comprehensive divergence metrics.

    Args:
        human_responses: Dictionary mapping option to count
        model_predictions: Dictionary mapping option to probability

    Returns:
        Dictionary with divergence metrics
    """
    options = list(human_responses.keys())

    if not options:
        return {
            "absolute_difference": 0.0,
            "jensen_shannon_divergence": 0.0,
            "sample_size": 0,
        }

    # Convert to arrays
    human_counts = np.array([human_responses.get(opt, 0) for opt in options])
    model_probs = np.array([model_predictions.get(opt, 0.0) for opt in options])

    # Normalize
    human_total = human_counts.sum()
    if human_total == 0:
        human_dist = np.zeros(len(options))
    else:
        human_dist = human_counts / human_total

    model_total = model_probs.sum()
    if model_total == 0:
        model_dist = np.ones(len(options)) / len(options)
    else:
        model_dist = model_probs / model_total

    # Calculate metrics
    abs_diff = absolute_difference(human_dist, model_dist)
    jsd = jensen_shannon_divergence(human_dist, model_dist)

    # Chi-squared test
    expected_counts = model_dist * human_total
    chi2, p_value = chi_squared_test(human_counts, expected_counts)

    return {
        "absolute_difference": abs_diff,
        "jensen_shannon_divergence": jsd,
        "chi2_statistic": chi2,
        "p_value": p_value,
        "sample_size": int(human_total),
        "human_distribution": human_dist.tolist(),
        "model_distribution": model_dist.tolist(),
        "options": options,
    }


def summarize_study_results(
    responses: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Summarize results from a study.

    Args:
        responses: List of response dictionaries

    Returns:
        Summary statistics
    """
    if not responses:
        return {
            "total_responses": 0,
            "mean_reaction_time_ms": 0.0,
            "choice_distribution": {},
        }

    total = len(responses)

    # Reaction times
    reaction_times = [r.get("reaction_time_ms", 0) for r in responses if "reaction_time_ms" in r]
    mean_rt = np.mean(reaction_times) if reaction_times else 0.0

    # Choice distribution
    choices = [r.get("choice", "") for r in responses if "choice" in r]
    choice_counts = {}
    for choice in choices:
        choice_counts[choice] = choice_counts.get(choice, 0) + 1

    # Confidence (if available)
    confidences = [r.get("confidence") for r in responses if r.get("confidence") is not None]
    mean_confidence = np.mean(confidences) if confidences else None

    return {
        "total_responses": total,
        "mean_reaction_time_ms": float(mean_rt),
        "choice_distribution": choice_counts,
        "mean_confidence": float(mean_confidence) if mean_confidence is not None else None,
    }
