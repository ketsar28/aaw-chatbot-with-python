"""
AI service factory for creating provider instances.

This module provides a factory for creating AI service instances
based on provider name.
"""

from typing import Optional
from .base import BaseAIService
from .openai_service import OpenAIService
from .anthropic_service import AnthropicService
from .google_service import GoogleService
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AIServiceFactory:
    """Factory for creating AI service instances."""

    @staticmethod
    def create(provider: str, settings: Settings) -> Optional[BaseAIService]:
        """
        Create AI service instance for the specified provider.

        Args:
            provider: Provider name (openai, anthropic, google)
            settings: Application settings

        Returns:
            AI service instance or None if provider not available

        Raises:
            ValueError: If provider is not supported
            ImportError: If required package is not installed
        """
        provider = provider.lower()

        try:
            if provider == "openai":
                if not settings.has_openai_key():
                    logger.warning("OpenAI API key not configured")
                    return None
                return OpenAIService(settings.openai_api_key)

            elif provider == "anthropic":
                if not settings.has_anthropic_key():
                    logger.warning("Anthropic API key not configured")
                    return None
                return AnthropicService(settings.anthropic_api_key)

            elif provider == "google":
                if not settings.has_google_key():
                    logger.warning("Google API key not configured")
                    return None
                return GoogleService(settings.google_api_key)

            else:
                raise ValueError(
                    f"Unsupported provider: {provider}. "
                    "Supported providers: openai, anthropic, google"
                )

        except ImportError as e:
            logger.error(f"Failed to create {provider} service: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating {provider} service: {e}")
            raise

    @staticmethod
    def get_available_providers(settings: Settings) -> list[str]:
        """
        Get list of available providers based on configured API keys.

        Args:
            settings: Application settings

        Returns:
            List of available provider names
        """
        return settings.get_available_providers()
