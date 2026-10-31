"""
Application configuration using pydantic-settings.

All configuration is loaded from environment variables with sensible defaults
for development. Production deployments MUST override SECRET_KEY and other
security-sensitive settings.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_env: str = Field(
        default="development", description="Environment: development, production, test"
    )
    debug: bool = Field(default=True, description="Enable debug mode")
    secret_key: str = Field(
        default="insecure-dev-key-change-in-production",
        description="Secret key for sessions and CSRF. MUST be changed in production.",
    )
    log_level: str = Field(default="INFO", description="Logging level")

    # Database
    database_url: str = Field(
        default="sqlite:///./mirageforge.db",
        description="Database connection URL",
    )

    # Admin
    admin_token: str | None = Field(
        default=None,
        description="Admin token for protected endpoints. If empty, admin endpoints are disabled.",
    )

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # Experiment
    default_study_id: int = Field(default=1, description="Default study ID for experiments")
    trials_per_session: int = Field(
        default=12, ge=1, le=100, description="Number of trials per session"
    )

    # ML Models
    enable_clip_backend: bool = Field(default=False, description="Enable CLIP vision backend")
    clip_model_name: str = Field(
        default="openai/clip-vit-base-patch32", description="CLIP model name"
    )

    # Rate Limiting
    rate_limit_rpm: int = Field(default=100, ge=1, description="Requests per minute per session")

    # Security
    csrf_secret: str = Field(
        default="csrf-dev-secret-change-in-production",
        description="CSRF secret key",
    )
    session_cookie_name: str = Field(
        default="mirageforge_session", description="Session cookie name"
    )
    session_cookie_secure: bool = Field(
        default=False, description="Use secure cookies (HTTPS only)"
    )

    # Paths
    artifacts_dir: Path = Field(
        default=Path("artifacts"), description="Directory for generated artifacts"
    )
    data_dir: Path = Field(default=Path("data"), description="Directory for data files")

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Warn if using default secret key in production."""
        if v == "insecure-dev-key-change-in-production":
            import warnings

            warnings.warn(
                "Using default SECRET_KEY. This is insecure for production. "
                "Set SECRET_KEY environment variable to a random string.",
                UserWarning,
                stacklevel=2,
            )
        return v

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        """Validate environment name."""
        allowed = {"development", "production", "test"}
        if v not in allowed:
            raise ValueError(f"app_env must be one of {allowed}, got {v}")
        return v

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    def is_admin_enabled(self) -> bool:
        """Check if admin endpoints are enabled."""
        return bool(self.admin_token)

    def verify_admin_token(self, token: str) -> bool:
        """Verify admin token."""
        if not self.admin_token:
            return False
        return token == self.admin_token


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def reset_settings_cache() -> None:
    """Reset settings cache (useful for testing)."""
    get_settings.cache_clear()
