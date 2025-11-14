"""
Application settings and configuration management.

This module handles loading and validating configuration from environment
variables using pydantic for type safety and validation.
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key")

    # Anthropic Configuration
    anthropic_api_key: Optional[str] = Field(None, description="Anthropic API key")

    # Google Gemini Configuration
    google_api_key: Optional[str] = Field(None, description="Google API key")

    # Application Configuration
    app_name: str = Field("AAW Master Chatbot", description="Application name")
    app_version: str = Field("2.0.0", description="Application version")
    environment: str = Field("development", description="Environment (development/production)")

    # Database Configuration
    database_url: str = Field(
        "sqlite:///./data/chatbot.db",
        description="Database connection URL"
    )

    # Logging Configuration
    log_level: str = Field("INFO", description="Logging level")
    log_file: str = Field("logs/chatbot.log", description="Log file path")

    # AI Model Configuration
    default_ai_provider: str = Field("openai", description="Default AI provider")
    default_model: str = Field("gpt-4", description="Default AI model")
    max_tokens: int = Field(4096, description="Maximum tokens per response")
    temperature: float = Field(0.7, description="Model temperature")

    # Rate Limiting
    max_requests_per_minute: int = Field(10, description="Max API requests per minute")

    # Session Configuration
    session_timeout: int = Field(3600, description="Session timeout in seconds")

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validate temperature is between 0 and 2."""
        if not 0 <= v <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        return v

    @field_validator("default_ai_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Validate AI provider is supported."""
        valid_providers = ["openai", "anthropic", "google"]
        if v.lower() not in valid_providers:
            raise ValueError(f"Provider must be one of: {', '.join(valid_providers)}")
        return v.lower()

    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.openai_api_key)

    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(self.anthropic_api_key)

    def has_google_key(self) -> bool:
        """Check if Google API key is configured."""
        return bool(self.google_api_key)

    def get_available_providers(self) -> list[str]:
        """Get list of configured AI providers."""
        providers = []
        if self.has_openai_key():
            providers.append("openai")
        if self.has_anthropic_key():
            providers.append("anthropic")
        if self.has_google_key():
            providers.append("google")
        return providers


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings: Application settings instance
    """
    return Settings()
