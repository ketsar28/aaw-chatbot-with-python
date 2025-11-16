"""
OpenAI service implementation.

This module provides integration with OpenAI's GPT models.
"""

from typing import List, Dict, Optional
from openai import OpenAI, OpenAIError

from .base import BaseAIService, AIResponse
from ..utils.logger import get_logger
from ..utils.token_counter import count_messages_tokens, estimate_cost

logger = get_logger(__name__)


class OpenAIService(BaseAIService):
    """Service for interacting with OpenAI API."""

    AVAILABLE_MODELS = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k"
    ]

    def __init__(self, api_key: str):
        """
        Initialize OpenAI service.

        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI service initialized")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> AIResponse:
        """
        Send chat request to OpenAI.

        Args:
            messages: List of message dictionaries
            model: Model to use (defaults to gpt-4)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            AIResponse with generated content

        Raises:
            OpenAIError: If API call fails
        """
        if model is None:
            model = "gpt-4"

        try:
            logger.debug(f"Sending request to OpenAI: model={model}, messages={len(messages)}")

            # Count input tokens
            input_tokens = count_messages_tokens(messages, model)

            # Make API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )

            # Extract response
            content = response.choices[0].message.content
            output_tokens = response.usage.completion_tokens if response.usage else 0
            total_tokens = response.usage.total_tokens if response.usage else input_tokens

            # Estimate cost
            cost = estimate_cost(input_tokens, output_tokens, "openai", model)

            logger.info(f"OpenAI response received: tokens={total_tokens}, cost=${cost:.4f}")

            return AIResponse(
                content=content,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost=cost,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id
                }
            )

        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI service: {e}")
            raise

    def get_available_models(self) -> List[str]:
        """
        Get list of available OpenAI models.

        Returns:
            List of model names
        """
        return self.AVAILABLE_MODELS

    def validate_api_key(self) -> bool:
        """
        Validate OpenAI API key.

        Returns:
            True if API key is valid
        """
        try:
            # Try to list models as a validation check
            self.client.models.list()
            logger.info("OpenAI API key validated successfully")
            return True
        except Exception as e:
            logger.error(f"OpenAI API key validation failed: {e}")
            return False
