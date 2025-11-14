"""
Anthropic Claude service implementation.

This module provides integration with Anthropic's Claude models.
"""

from typing import List, Dict, Optional
try:
    from anthropic import Anthropic, AnthropicError
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .base import BaseAIService, AIResponse
from ..utils.logger import get_logger
from ..utils.token_counter import count_messages_tokens, estimate_cost

logger = get_logger(__name__)


class AnthropicService(BaseAIService):
    """Service for interacting with Anthropic Claude API."""

    AVAILABLE_MODELS = [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]

    def __init__(self, api_key: str):
        """
        Initialize Anthropic service.

        Args:
            api_key: Anthropic API key

        Raises:
            ImportError: If anthropic package is not installed
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "anthropic package not installed. "
                "Install it with: pip install anthropic"
            )

        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        logger.info("Anthropic service initialized")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> AIResponse:
        """
        Send chat request to Anthropic Claude.

        Args:
            messages: List of message dictionaries
            model: Model to use (defaults to claude-3-sonnet)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            AIResponse with generated content

        Raises:
            AnthropicError: If API call fails
        """
        if model is None:
            model = "claude-3-sonnet-20240229"

        try:
            # Extract system message if present
            system_message = ""
            chat_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    chat_messages.append(msg)

            logger.debug(f"Sending request to Anthropic: model={model}, messages={len(chat_messages)}")

            # Count input tokens
            input_tokens = count_messages_tokens(messages, model)

            # Make API call
            response = self.client.messages.create(
                model=model,
                messages=chat_messages,
                system=system_message if system_message else None,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Extract response
            content = response.content[0].text
            output_tokens = response.usage.output_tokens
            total_tokens = response.usage.input_tokens + output_tokens

            # Estimate cost
            cost = estimate_cost(input_tokens, output_tokens, "anthropic", model)

            logger.info(f"Anthropic response received: tokens={total_tokens}, cost=${cost:.4f}")

            return AIResponse(
                content=content,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost=cost,
                metadata={
                    "stop_reason": response.stop_reason,
                    "response_id": response.id
                }
            )

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    def get_available_models(self) -> List[str]:
        """
        Get list of available Anthropic models.

        Returns:
            List of model names
        """
        return self.AVAILABLE_MODELS

    def validate_api_key(self) -> bool:
        """
        Validate Anthropic API key.

        Returns:
            True if API key is valid
        """
        try:
            # Try a minimal API call as validation
            self.client.messages.create(
                model="claude-3-haiku-20240307",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            logger.info("Anthropic API key validated successfully")
            return True
        except Exception as e:
            logger.error(f"Anthropic API key validation failed: {e}")
            return False
