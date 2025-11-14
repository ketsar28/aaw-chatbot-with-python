"""
Token counting and cost estimation utilities.

This module provides utilities for counting tokens and estimating
API costs for different AI providers.
"""

import tiktoken
from typing import List, Dict, Optional


# Pricing per 1K tokens (as of 2024)
PRICING = {
    "openai": {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    },
    "anthropic": {
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
    },
    "google": {
        "gemini-pro": {"input": 0.00025, "output": 0.0005},
        "gemini-pro-vision": {"input": 0.00025, "output": 0.0005},
    }
}


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text string.

    Args:
        text: Text to count tokens for
        model: Model name for tokenization

    Returns:
        Number of tokens
    """
    try:
        # Use tiktoken for OpenAI models
        if "gpt" in model.lower():
            encoding = tiktoken.encoding_for_model(model)
        else:
            # Default to cl100k_base for other models
            encoding = tiktoken.get_encoding("cl100k_base")

        return len(encoding.encode(text))
    except Exception:
        # Fallback: rough estimation (1 token ≈ 4 characters)
        return len(text) // 4


def count_messages_tokens(messages: List[Dict[str, str]], model: str = "gpt-4") -> int:
    """
    Count tokens in a list of messages.

    Args:
        messages: List of message dictionaries
        model: Model name for tokenization

    Returns:
        Total number of tokens
    """
    total_tokens = 0
    for message in messages:
        # Count tokens in content
        total_tokens += count_tokens(message.get("content", ""), model)
        # Add overhead for role and formatting (roughly 4 tokens per message)
        total_tokens += 4

    return total_tokens


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    provider: str,
    model: str
) -> float:
    """
    Estimate the cost of an API call.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        provider: AI provider name
        model: Model name

    Returns:
        Estimated cost in USD
    """
    provider = provider.lower()
    model = model.lower()

    if provider not in PRICING:
        return 0.0

    provider_pricing = PRICING[provider]

    # Find matching model pricing
    model_pricing = None
    for price_model, prices in provider_pricing.items():
        if price_model in model:
            model_pricing = prices
            break

    if not model_pricing:
        return 0.0

    input_cost = (input_tokens / 1000) * model_pricing["input"]
    output_cost = (output_tokens / 1000) * model_pricing["output"]

    return input_cost + output_cost


def get_model_pricing(provider: str, model: str) -> Optional[Dict[str, float]]:
    """
    Get pricing information for a specific model.

    Args:
        provider: AI provider name
        model: Model name

    Returns:
        Pricing dictionary or None if not found
    """
    provider = provider.lower()
    model = model.lower()

    if provider not in PRICING:
        return None

    for price_model, prices in PRICING[provider].items():
        if price_model in model:
            return prices

    return None
