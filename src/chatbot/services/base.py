"""
Base AI service interface.

This module defines the abstract base class for AI service providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class AIResponse:
    """
    Standardized response from AI providers.

    Attributes:
        content: Response text content
        model: Model used for generation
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        total_tokens: Total tokens used
        cost: Estimated cost in USD
        metadata: Additional provider-specific metadata
    """
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    metadata: Optional[Dict] = None


class BaseAIService(ABC):
    """Abstract base class for AI service providers."""

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> AIResponse:
        """
        Send chat request to AI provider.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (provider-specific)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            AIResponse with generated content and metadata

        Raises:
            Exception: If API call fails
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get list of available models for this provider.

        Returns:
            List of model names
        """
        pass

    @abstractmethod
    def validate_api_key(self) -> bool:
        """
        Validate API key is configured and working.

        Returns:
            True if API key is valid, False otherwise
        """
        pass

    def get_provider_name(self) -> str:
        """
        Get the name of this provider.

        Returns:
            Provider name
        """
        return self.__class__.__name__.replace("Service", "").lower()
