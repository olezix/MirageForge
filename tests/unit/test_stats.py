"""
Unit tests for statistical analysis functions.
"""

import numpy as np

from mirageforge.experiment.stats import (
    absolute_difference,
    benjamini_hochberg,
    bootstrap_ci_difference,
    calculate_divergence_metrics,
    jensen_shannon_divergence,
    wilson_ci_proportion,
)


class TestWilsonCI:
    """Tests for Wilson confidence interval."""

    def test_wilson_ci_basic(self):
        """Test basic Wilson CI calculation."""
        proportion, lower, upper = wilson_ci_proportion(successes=50, total=100)

        assert proportion == 0.5
        assert lower < proportion < upper
        assert 0.0 <= lower <= 1.0
        assert 0.0 <= upper <= 1.0

    def test_wilson_ci_zero_total(self):
        """Test Wilson CI with zero total."""
        proportion, lower, upper = wilson_ci_proportion(successes=0, total=0)

        assert proportion == 0.0
        assert lower == 0.0
        assert upper == 0.0

    def test_wilson_ci_all_successes(self):
        """Test Wilson CI with all successes."""
        proportion, lower, upper = wilson_ci_proportion(successes=100, total=100)

        assert proportion == 1.0
        assert lower < 1.0
        assert upper == 1.0

    def test_wilson_ci_no_successes(self):
        """Test Wilson CI with no successes."""
        proportion, lower, upper = wilson_ci_proportion(successes=0, total=100)

        assert proportion == 0.0
        assert lower < 0.01  # Should be very close to 0
        assert upper > 0.0


class TestBootstrapCI:
    """Tests for bootstrap confidence interval."""

    def test_bootstrap_ci_basic(self):
        """Test basic bootstrap CI calculation."""
        human = np.array([1, 0, 1, 1, 0, 1, 0, 1])
        model = np.array([0.6, 0.4, 0.7, 0.8, 0.3, 0.6, 0.5, 0.7])

        diff, lower, upper = bootstrap_ci_difference(human, model, num_samples=100, seed=42)

        assert lower <= diff <= upper

    def test_bootstrap_ci_empty(self):
        """Test bootstrap CI with empty arrays."""
        diff, lower, upper = bootstrap_ci_difference(np.array([]), np.array([]))

        assert diff == 0.0
        assert lower == 0.0
        assert upper == 0.0


class TestJensenShannonDivergence:
    """Tests for Jensen-Shannon divergence."""

    def test_jsd_identical_distributions(self):
        """Test JSD with identical distributions."""
        p = np.array([0.5, 0.5])
        q = np.array([0.5, 0.5])

        jsd = jensen_shannon_divergence(p, q)

        assert jsd == 0.0

    def test_jsd_different_distributions(self):
        """Test JSD with different distributions."""
        p = np.array([0.9, 0.1])
        q = np.array([0.1, 0.9])

        jsd = jensen_shannon_divergence(p, q)

        assert 0.0 < jsd <= 1.0

    def test_jsd_symmetry(self):
        """Test JSD symmetry."""
        p = np.array([0.7, 0.3])
        q = np.array([0.4, 0.6])

        jsd_pq = jensen_shannon_divergence(p, q)
        jsd_qp = jensen_shannon_divergence(q, p)

        assert abs(jsd_pq - jsd_qp) < 1e-10


class TestAbsoluteDifference:
    """Tests for absolute difference."""

    def test_absolute_difference_identical(self):
        """Test absolute difference with identical distributions."""
        p = np.array([0.5, 0.5])
        q = np.array([0.5, 0.5])

        diff = absolute_difference(p, q)

        assert diff == 0.0

    def test_absolute_difference_different(self):
        """Test absolute difference with different distributions."""
        p = np.array([0.8, 0.2])
        q = np.array([0.3, 0.7])

        diff = absolute_difference(p, q)

        assert diff > 0.0


class TestBenjaminiHochberg:
    """Tests for Benjamini-Hochberg correction."""

    def test_bh_no_significant(self):
        """Test BH with no significant p-values."""
        p_values = [0.5, 0.6, 0.7, 0.8]
        results = benjamini_hochberg(p_values, alpha=0.05)

        assert len(results) == 4
        assert all(not significant for _, significant in results)

    def test_bh_some_significant(self):
        """Test BH with some significant p-values."""
        p_values = [0.001, 0.01, 0.05, 0.5]
        results = benjamini_hochberg(p_values, alpha=0.05)

        assert len(results) == 4
        # At least the smallest p-value should be significant
        assert results[0][1] is True

    def test_bh_empty(self):
        """Test BH with empty list."""
        results = benjamini_hochberg([])
        assert results == []


class TestDivergenceMetrics:
    """Tests for divergence metrics calculation."""

    def test_calculate_divergence_metrics_basic(self):
        """Test basic divergence metrics calculation."""
        human_responses = {"Option A": 60, "Option B": 40}
        model_predictions = {"Option A": 0.55, "Option B": 0.45}

        metrics = calculate_divergence_metrics(human_responses, model_predictions)

        assert "absolute_difference" in metrics
        assert "jensen_shannon_divergence" in metrics
        assert "sample_size" in metrics
        assert metrics["sample_size"] == 100

    def test_calculate_divergence_metrics_empty(self):
        """Test divergence metrics with empty data."""
        metrics = calculate_divergence_metrics({}, {})

        assert metrics["sample_size"] == 0
        assert metrics["absolute_difference"] == 0.0
        assert metrics["jensen_shannon_divergence"] == 0.0
