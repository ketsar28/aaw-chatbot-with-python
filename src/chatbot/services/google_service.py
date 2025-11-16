"""
Google Gemini service implementation.

This module provides integration with Google's Gemini models.
"""

from typing import List, Dict, Optional
try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from .base import BaseAIService, AIResponse
from ..utils.logger import get_logger
from ..utils.token_counter import count_messages_tokens, estimate_cost

logger = get_logger(__name__)


class GoogleService(BaseAIService):
    """Service for interacting with Google Gemini API."""

    AVAILABLE_MODELS = [
        "gemini-pro",
        "gemini-pro-vision"
    ]

    def __init__(self, api_key: str):
        """
        Initialize Google Gemini service.

        Args:
            api_key: Google API key

        Raises:
            ImportError: If google-generativeai package is not installed
        """
        if not GOOGLE_AVAILABLE:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install it with: pip install google-generativeai"
            )

        self.api_key = api_key
        genai.configure(api_key=api_key)
        logger.info("Google Gemini service initialized")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> AIResponse:
        """
        Send chat request to Google Gemini.

        Args:
            messages: List of message dictionaries
            model: Model to use (defaults to gemini-pro)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            AIResponse with generated content

        Raises:
            Exception: If API call fails
        """
        if model is None:
            model = "gemini-pro"

        try:
            # Convert messages to Gemini format
            gemini_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    # Gemini doesn't have system role, prepend to first user message
                    continue
                elif msg["role"] == "user":
                    gemini_messages.append({
                        "role": "user",
                        "parts": [msg["content"]]
                    })
                elif msg["role"] == "assistant":
                    gemini_messages.append({
                        "role": "model",
                        "parts": [msg["content"]]
                    })

            logger.debug(f"Sending request to Google: model={model}, messages={len(gemini_messages)}")

            # Count input tokens
            input_tokens = count_messages_tokens(messages, model)

            # Configure model
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            # Create model instance
            gemini_model = genai.GenerativeModel(
                model_name=model,
                generation_config=generation_config
            )

            # Start chat
            chat = gemini_model.start_chat(history=gemini_messages[:-1] if len(gemini_messages) > 1 else [])

            # Send message
            last_message = gemini_messages[-1]["parts"][0] if gemini_messages else ""
            response = chat.send_message(last_message)

            # Extract response
            content = response.text

            # Estimate tokens (Gemini doesn't provide token counts directly)
            output_tokens = len(content) // 4  # Rough estimation
            total_tokens = input_tokens + output_tokens

            # Estimate cost
            cost = estimate_cost(input_tokens, output_tokens, "google", model)

            logger.info(f"Google response received: tokens≈{total_tokens}, cost≈${cost:.4f}")

            return AIResponse(
                content=content,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost=cost,
                metadata={
                    "finish_reason": "stop"
                }
            )

        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            raise

    def get_available_models(self) -> List[str]:
        """
        Get list of available Google models.

        Returns:
            List of model names
        """
        return self.AVAILABLE_MODELS

    def validate_api_key(self) -> bool:
        """
        Validate Google API key.

        Returns:
            True if API key is valid
        """
        try:
            # Try listing models as validation
            genai.list_models()
            logger.info("Google API key validated successfully")
            return True
        except Exception as e:
            logger.error(f"Google API key validation failed: {e}")
            return False
