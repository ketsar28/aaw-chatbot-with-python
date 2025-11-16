"""
Repository for conversation and message database operations.

This module provides methods for CRUD operations on conversations
and messages.
"""

from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.conversation import Conversation, Message, MessageRole
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ConversationRepository:
    """Repository for conversation database operations."""

    def __init__(self, session: Session):
        """
        Initialize conversation repository.

        Args:
            session: Database session
        """
        self.session = session

    def create_conversation(
        self,
        title: str,
        provider: str,
        model: str
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            title: Conversation title
            provider: AI provider name
            model: AI model name

        Returns:
            Created conversation
        """
        try:
            conversation = Conversation(
                title=title,
                provider=provider,
                model=model
            )
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)

            logger.info(f"Created conversation: {conversation.id}")
            return conversation

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create conversation: {e}")
            raise

    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """
        Get conversation by ID.

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation or None if not found
        """
        return self.session.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

    def get_all_conversations(self, limit: int = 50) -> List[Conversation]:
        """
        Get all conversations ordered by most recent.

        Args:
            limit: Maximum number of conversations to return

        Returns:
            List of conversations
        """
        return self.session.query(Conversation).order_by(
            Conversation.updated_at.desc()
        ).limit(limit).all()

    def update_conversation(
        self,
        conversation_id: int,
        title: Optional[str] = None,
        total_tokens: Optional[int] = None,
        total_cost: Optional[float] = None
    ) -> Optional[Conversation]:
        """
        Update conversation details.

        Args:
            conversation_id: Conversation ID
            title: New title (optional)
            total_tokens: New total tokens (optional)
            total_cost: New total cost (optional)

        Returns:
            Updated conversation or None if not found
        """
        try:
            conversation = self.get_conversation(conversation_id)
            if not conversation:
                return None

            if title is not None:
                conversation.title = title
            if total_tokens is not None:
                conversation.total_tokens = total_tokens
            if total_cost is not None:
                conversation.total_cost = total_cost

            conversation.updated_at = datetime.utcnow()
            self.session.commit()
            self.session.refresh(conversation)

            logger.info(f"Updated conversation: {conversation_id}")
            return conversation

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update conversation: {e}")
            raise

    def delete_conversation(self, conversation_id: int) -> bool:
        """
        Delete conversation and all its messages.

        Args:
            conversation_id: Conversation ID

        Returns:
            True if deleted, False if not found
        """
        try:
            conversation = self.get_conversation(conversation_id)
            if not conversation:
                return False

            self.session.delete(conversation)
            self.session.commit()

            logger.info(f"Deleted conversation: {conversation_id}")
            return True

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to delete conversation: {e}")
            raise

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        tokens: int = 0
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            conversation_id: Conversation ID
            role: Message role (system, user, assistant)
            content: Message content
            tokens: Number of tokens in message

        Returns:
            Created message
        """
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                tokens=tokens
            )
            self.session.add(message)

            # Update conversation's updated_at timestamp
            conversation = self.get_conversation(conversation_id)
            if conversation:
                conversation.updated_at = datetime.utcnow()

            self.session.commit()
            self.session.refresh(message)

            logger.debug(f"Added message to conversation {conversation_id}")
            return message

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add message: {e}")
            raise

    def get_messages(self, conversation_id: int) -> List[Message]:
        """
        Get all messages for a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of messages ordered by creation time
        """
        return self.session.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()

    def get_messages_as_dicts(self, conversation_id: int) -> List[Dict[str, str]]:
        """
        Get messages as dictionaries for API calls.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of message dictionaries
        """
        messages = self.get_messages(conversation_id)
        return [msg.to_dict() for msg in messages]

    def clear_messages(self, conversation_id: int) -> bool:
        """
        Clear all messages from a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            True if messages cleared, False if conversation not found
        """
        try:
            conversation = self.get_conversation(conversation_id)
            if not conversation:
                return False

            self.session.query(Message).filter(
                Message.conversation_id == conversation_id
            ).delete()
            self.session.commit()

            logger.info(f"Cleared messages for conversation: {conversation_id}")
            return True

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to clear messages: {e}")
            raise
