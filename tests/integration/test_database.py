"""Integration tests for database operations."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chatbot.models.conversation import Base, Conversation, Message
from chatbot.repositories.conversation_repository import ConversationRepository


@pytest.fixture
def db_session():
    """Create a test database session."""
    # Use in-memory SQLite database for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()


def test_create_conversation(db_session):
    """Test creating a conversation."""
    repo = ConversationRepository(db_session)

    conversation = repo.create_conversation(
        title="Test Conversation",
        provider="openai",
        model="gpt-4"
    )

    assert conversation.id is not None
    assert conversation.title == "Test Conversation"
    assert conversation.provider == "openai"
    assert conversation.model == "gpt-4"


def test_get_conversation(db_session):
    """Test retrieving a conversation."""
    repo = ConversationRepository(db_session)

    # Create conversation
    created = repo.create_conversation(
        title="Test",
        provider="openai",
        model="gpt-4"
    )

    # Retrieve conversation
    retrieved = repo.get_conversation(created.id)

    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.title == created.title


def test_add_message(db_session):
    """Test adding a message to a conversation."""
    repo = ConversationRepository(db_session)

    # Create conversation
    conversation = repo.create_conversation(
        title="Test",
        provider="openai",
        model="gpt-4"
    )

    # Add message
    message = repo.add_message(
        conversation_id=conversation.id,
        role="user",
        content="Hello!",
        tokens=10
    )

    assert message.id is not None
    assert message.conversation_id == conversation.id
    assert message.role == "user"
    assert message.content == "Hello!"


def test_get_messages(db_session):
    """Test retrieving messages."""
    repo = ConversationRepository(db_session)

    # Create conversation
    conversation = repo.create_conversation(
        title="Test",
        provider="openai",
        model="gpt-4"
    )

    # Add messages
    repo.add_message(conversation.id, "user", "Hello", 5)
    repo.add_message(conversation.id, "assistant", "Hi there!", 8)

    # Retrieve messages
    messages = repo.get_messages(conversation.id)

    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"


def test_delete_conversation(db_session):
    """Test deleting a conversation."""
    repo = ConversationRepository(db_session)

    # Create conversation with messages
    conversation = repo.create_conversation(
        title="Test",
        provider="openai",
        model="gpt-4"
    )
    repo.add_message(conversation.id, "user", "Test", 5)

    # Delete conversation
    result = repo.delete_conversation(conversation.id)

    assert result is True

    # Verify deletion
    retrieved = repo.get_conversation(conversation.id)
    assert retrieved is None
