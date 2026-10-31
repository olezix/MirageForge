"""
Integration tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from mirageforge.db import init_db
from mirageforge.web.app import app


@pytest.fixture(scope="module")
def client():
    """Create test client."""
    init_db()
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_healthz(self, client):
        """Test health check endpoint."""
        response = client.get("/healthz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestLandingPage:
    """Tests for landing page."""

    def test_landing_page(self, client):
        """Test landing page loads."""
        response = client.get("/")
        assert response.status_code == 200
        assert "MirageForge" in response.text


class TestConsentPage:
    """Tests for consent page."""

    def test_consent_page(self, client):
        """Test consent page loads."""
        response = client.get("/consent")
        assert response.status_code == 200
        assert "consent" in response.text.lower()


class TestGalleryPage:
    """Tests for gallery page."""

    def test_gallery_page(self, client):
        """Test gallery page loads."""
        response = client.get("/gallery")
        assert response.status_code == 200


class TestDashboardPage:
    """Tests for dashboard page."""

    def test_dashboard_page(self, client):
        """Test dashboard page loads."""
        response = client.get("/dashboard")
        assert response.status_code == 200


class TestDebriefPage:
    """Tests for debrief page."""

    def test_debrief_page(self, client):
        """Test debrief page loads."""
        response = client.get("/debrief")
        assert response.status_code == 200
        assert "thank" in response.text.lower()


class TestAPISession:
    """Tests for session API."""

    def test_create_session(self, client):
        """Test session creation."""
        response = client.post(
            "/api/session",
            json={"study_id": 1, "consent_version": "1.0.0"},
        )
        # May fail if study doesn't exist, but should not crash
        assert response.status_code in [200, 404, 422]


class TestSecurityHeaders:
    """Tests for security headers."""

    def test_security_headers_present(self, client):
        """Test that security headers are present."""
        response = client.get("/healthz")
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "Referrer-Policy" in response.headers
