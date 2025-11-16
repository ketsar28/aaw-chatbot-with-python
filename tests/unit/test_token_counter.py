"""Unit tests for token counting utilities."""

import pytest
from chatbot.utils.token_counter import (
    count_tokens,
    count_messages_tokens,
    estimate_cost,
    get_model_pricing
)


def test_count_tokens():
    """Test token counting."""
    text = "Hello, world!"
    tokens = count_tokens(text, model="gpt-4")
    assert tokens > 0
    assert isinstance(tokens, int)


def test_count_messages_tokens():
    """Test counting tokens in messages."""
    messages = [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"}
    ]

    tokens = count_messages_tokens(messages, model="gpt-4")
    assert tokens > 0
    assert isinstance(tokens, int)


def test_estimate_cost_openai():
    """Test cost estimation for OpenAI."""
    cost = estimate_cost(
        input_tokens=1000,
        output_tokens=500,
        provider="openai",
        model="gpt-4"
    )

    assert cost > 0
    assert isinstance(cost, float)


def test_estimate_cost_anthropic():
    """Test cost estimation for Anthropic."""
    cost = estimate_cost(
        input_tokens=1000,
        output_tokens=500,
        provider="anthropic",
        model="claude-3-sonnet"
    )

    assert cost > 0
    assert isinstance(cost, float)


def test_estimate_cost_invalid_provider():
    """Test cost estimation with invalid provider."""
    cost = estimate_cost(
        input_tokens=1000,
        output_tokens=500,
        provider="invalid",
        model="some-model"
    )

    assert cost == 0.0


def test_get_model_pricing():
    """Test getting model pricing."""
    pricing = get_model_pricing("openai", "gpt-4")
    assert pricing is not None
    assert "input" in pricing
    assert "output" in pricing

    # Invalid provider
    pricing = get_model_pricing("invalid", "model")
    assert pricing is None
