"""Unit tests for configuration management."""

import pytest
from pydantic import ValidationError
from chatbot.config.settings import Settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()
    assert settings.app_name == "AAW Master Chatbot"
    assert settings.app_version == "2.0.0"
    assert settings.environment == "development"
    assert settings.default_ai_provider == "openai"
    assert settings.temperature == 0.7


def test_temperature_validation():
    """Test temperature validation."""
    # Valid temperatures
    Settings(temperature=0.0)
    Settings(temperature=1.0)
    Settings(temperature=2.0)

    # Invalid temperature
    with pytest.raises(ValidationError):
        Settings(temperature=-0.1)

    with pytest.raises(ValidationError):
        Settings(temperature=2.1)


def test_provider_validation():
    """Test provider validation."""
    # Valid providers
    Settings(default_ai_provider="openai")
    Settings(default_ai_provider="anthropic")
    Settings(default_ai_provider="google")

    # Invalid provider
    with pytest.raises(ValidationError):
        Settings(default_ai_provider="invalid")


def test_api_key_checks():
    """Test API key availability checks."""
    settings = Settings(
        openai_api_key="test-key",
        anthropic_api_key=None,
        google_api_key=None
    )

    assert settings.has_openai_key() is True
    assert settings.has_anthropic_key() is False
    assert settings.has_google_key() is False


def test_get_available_providers():
    """Test getting available providers."""
    settings = Settings(
        openai_api_key="key1",
        anthropic_api_key="key2",
        google_api_key=None
    )

    providers = settings.get_available_providers()
    assert "openai" in providers
    assert "anthropic" in providers
    assert "google" not in providers
