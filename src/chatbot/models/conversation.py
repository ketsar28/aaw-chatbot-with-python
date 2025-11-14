"""
Data models for conversations and messages.

This module defines the database models for storing conversations
and messages using SQLAlchemy ORM.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class MessageRole(str, Enum):
    """Enumeration of message roles."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Conversation(Base):
    """
    Conversation model for storing chat sessions.

    Attributes:
        id: Unique conversation identifier
        title: Conversation title
        provider: AI provider used (openai, anthropic, google)
        model: AI model used
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated
        total_tokens: Total tokens used in conversation
        total_cost: Estimated cost of conversation
        messages: Related messages in the conversation
    """

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)

    # Relationship
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation of conversation."""
        return f"<Conversation(id={self.id}, title='{self.title}', provider='{self.provider}')>"


class Message(Base):
    """
    Message model for storing individual chat messages.

    Attributes:
        id: Unique message identifier
        conversation_id: Foreign key to conversation
        role: Message role (system, user, assistant)
        content: Message content
        tokens: Number of tokens in message
        created_at: Timestamp when message was created
        conversation: Related conversation
    """

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self) -> str:
        """String representation of message."""
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, role='{self.role}', content='{content_preview}')>"

    def to_dict(self) -> dict:
        """
        Convert message to dictionary format.

        Returns:
            Dictionary representation of message
        """
        return {
            "role": self.role,
            "content": self.content
        }
