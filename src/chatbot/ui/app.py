"""
Main Streamlit application.

This module contains the main UI logic for the chatbot application
with support for multiple AI providers and conversation management.
"""

import streamlit as st
from typing import Optional, List, Dict
from datetime import datetime

from ..config.settings import get_settings
from ..repositories.database import get_db
from ..repositories.conversation_repository import ConversationRepository
from ..services.ai_service_factory import AIServiceFactory
from ..utils.logger import setup_logger, get_logger

# Initialize logger
settings = get_settings()
setup_logger(log_level=settings.log_level, log_file=settings.log_file)
logger = get_logger(__name__)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = settings.default_ai_provider

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = settings.default_model

    if "temperature" not in st.session_state:
        st.session_state.temperature = settings.temperature

    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = settings.max_tokens

    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0

    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0


def render_sidebar():
    """Render sidebar with settings and conversation management."""
    with st.sidebar:
        st.title("⚙️ Settings")

        # Get available providers
        available_providers = AIServiceFactory.get_available_providers(settings)

        if not available_providers:
            st.error("No AI providers configured! Please add API keys to .env file.")
            st.stop()

        # Provider selection
        provider_options = {
            "openai": "🤖 OpenAI (GPT)",
            "anthropic": "🧠 Anthropic (Claude)",
            "google": "🔮 Google (Gemini)"
        }

        available_options = {k: v for k, v in provider_options.items() if k in available_providers}

        selected_provider = st.selectbox(
            "AI Provider",
            options=list(available_options.keys()),
            format_func=lambda x: available_options[x],
            index=list(available_options.keys()).index(st.session_state.selected_provider)
            if st.session_state.selected_provider in available_options else 0
        )

        # Update provider if changed
        if selected_provider != st.session_state.selected_provider:
            st.session_state.selected_provider = selected_provider
            # Reset model selection when provider changes
            if selected_provider == "openai":
                st.session_state.selected_model = "gpt-4"
            elif selected_provider == "anthropic":
                st.session_state.selected_model = "claude-3-sonnet-20240229"
            elif selected_provider == "google":
                st.session_state.selected_model = "gemini-pro"

        # Model selection based on provider
        model_options = {
            "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            "google": ["gemini-pro", "gemini-pro-vision"]
        }

        st.session_state.selected_model = st.selectbox(
            "Model",
            options=model_options.get(selected_provider, []),
            index=0
        )

        st.divider()

        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            st.session_state.temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=float(st.session_state.temperature),
                step=0.1,
                help="Controls randomness. Lower = more focused, Higher = more creative"
            )

            st.session_state.max_tokens = st.number_input(
                "Max Tokens",
                min_value=100,
                max_value=8192,
                value=int(st.session_state.max_tokens),
                step=100,
                help="Maximum length of the response"
            )

        st.divider()

        # Conversation management
        st.subheader("💬 Conversations")

        # New conversation button
        if st.button("➕ New Conversation", use_container_width=True):
            create_new_conversation()

        # Load conversations
        db_manager = get_db()
        with next(db_manager.get_session()) as session:
            repo = ConversationRepository(session)
            conversations = repo.get_all_conversations(limit=20)

        # Display conversations
        if conversations:
            for conv in conversations:
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"📝 {conv.title[:30]}...",
                        key=f"load_{conv.id}",
                        use_container_width=True
                    ):
                        load_conversation(conv.id)
                with col2:
                    if st.button("🗑️", key=f"delete_{conv.id}"):
                        delete_conversation(conv.id)

        st.divider()

        # Statistics
        st.subheader("📊 Session Stats")
        st.metric("Total Tokens", f"{st.session_state.total_tokens:,}")
        st.metric("Estimated Cost", f"${st.session_state.total_cost:.4f}")


def create_new_conversation():
    """Create a new conversation."""
    try:
        db_manager = get_db()
        with next(db_manager.get_session()) as session:
            repo = ConversationRepository(session)

            # Generate title
            title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            # Create conversation
            conversation = repo.create_conversation(
                title=title,
                provider=st.session_state.selected_provider,
                model=st.session_state.selected_model
            )

            # Update session state
            st.session_state.current_conversation_id = conversation.id
            st.session_state.messages = []
            st.session_state.total_cost = 0.0
            st.session_state.total_tokens = 0

            logger.info(f"Created new conversation: {conversation.id}")
            st.rerun()

    except Exception as e:
        logger.error(f"Failed to create conversation: {e}")
        st.error(f"Failed to create conversation: {e}")


def load_conversation(conversation_id: int):
    """Load an existing conversation."""
    try:
        db_manager = get_db()
        with next(db_manager.get_session()) as session:
            repo = ConversationRepository(session)

            # Get conversation
            conversation = repo.get_conversation(conversation_id)
            if not conversation:
                st.error("Conversation not found")
                return

            # Load messages
            messages = repo.get_messages_as_dicts(conversation_id)

            # Update session state
            st.session_state.current_conversation_id = conversation_id
            st.session_state.messages = messages
            st.session_state.selected_provider = conversation.provider
            st.session_state.selected_model = conversation.model
            st.session_state.total_cost = conversation.total_cost
            st.session_state.total_tokens = conversation.total_tokens

            logger.info(f"Loaded conversation: {conversation_id}")
            st.rerun()

    except Exception as e:
        logger.error(f"Failed to load conversation: {e}")
        st.error(f"Failed to load conversation: {e}")


def delete_conversation(conversation_id: int):
    """Delete a conversation."""
    try:
        db_manager = get_db()
        with next(db_manager.get_session()) as session:
            repo = ConversationRepository(session)
            repo.delete_conversation(conversation_id)

            # If current conversation was deleted, reset
            if st.session_state.current_conversation_id == conversation_id:
                st.session_state.current_conversation_id = None
                st.session_state.messages = []
                st.session_state.total_cost = 0.0
                st.session_state.total_tokens = 0

            logger.info(f"Deleted conversation: {conversation_id}")
            st.rerun()

    except Exception as e:
        logger.error(f"Failed to delete conversation: {e}")
        st.error(f"Failed to delete conversation: {e}")


def render_chat():
    """Render the main chat interface."""
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Send a message..."):
        # Ensure we have a conversation
        if st.session_state.current_conversation_id is None:
            create_new_conversation()
            # Add system message
            system_message = {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
            st.session_state.messages.insert(0, system_message)

            # Save system message to database
            db_manager = get_db()
            with next(db_manager.get_session()) as session:
                repo = ConversationRepository(session)
                repo.add_message(
                    conversation_id=st.session_state.current_conversation_id,
                    role="system",
                    content=system_message["content"]
                )

        # Add user message
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Create AI service
                    ai_service = AIServiceFactory.create(
                        st.session_state.selected_provider,
                        settings
                    )

                    if not ai_service:
                        st.error("AI service not available. Check your API key configuration.")
                        return

                    # Get response
                    response = ai_service.chat(
                        messages=st.session_state.messages,
                        model=st.session_state.selected_model,
                        temperature=st.session_state.temperature,
                        max_tokens=st.session_state.max_tokens
                    )

                    # Display response
                    st.markdown(response.content)

                    # Add assistant message
                    assistant_message = {"role": "assistant", "content": response.content}
                    st.session_state.messages.append(assistant_message)

                    # Update statistics
                    st.session_state.total_tokens += response.total_tokens
                    st.session_state.total_cost += response.cost

                    # Save to database
                    db_manager = get_db()
                    with next(db_manager.get_session()) as session:
                        repo = ConversationRepository(session)

                        # Save user message
                        repo.add_message(
                            conversation_id=st.session_state.current_conversation_id,
                            role="user",
                            content=prompt,
                            tokens=response.input_tokens
                        )

                        # Save assistant message
                        repo.add_message(
                            conversation_id=st.session_state.current_conversation_id,
                            role="assistant",
                            content=response.content,
                            tokens=response.output_tokens
                        )

                        # Update conversation totals
                        repo.update_conversation(
                            conversation_id=st.session_state.current_conversation_id,
                            total_tokens=st.session_state.total_tokens,
                            total_cost=st.session_state.total_cost
                        )

                    logger.info(f"Generated response: {response.total_tokens} tokens, ${response.cost:.4f}")

                except Exception as e:
                    logger.error(f"Error generating response: {e}")
                    st.error(f"Error: {str(e)}")


def run_app():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title=f"{settings.app_name} v{settings.app_version}",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    initialize_session_state()

    # Render sidebar
    render_sidebar()

    # Main content
    st.title(f"🤖 {settings.app_name}")
    st.caption(f"Multi-Provider AI Chatbot | v{settings.app_version}")

    # Info banner
    if st.session_state.current_conversation_id:
        st.info(
            f"💬 Active conversation | "
            f"Provider: **{st.session_state.selected_provider.upper()}** | "
            f"Model: **{st.session_state.selected_model}**"
        )
    else:
        st.info("👋 Welcome! Start a new conversation or select an existing one from the sidebar.")

    # Render chat
    render_chat()


if __name__ == "__main__":
    run_app()
