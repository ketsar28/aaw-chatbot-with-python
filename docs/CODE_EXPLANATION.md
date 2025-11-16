# AAW Master Chatbot - Code Explanation

This document provides a detailed explanation of the codebase architecture and how different components work together.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Component Breakdown](#component-breakdown)
4. [Data Flow](#data-flow)
5. [Key Design Decisions](#key-design-decisions)

---

## Project Overview

AAW Master Chatbot is a production-ready chatbot application built with:
- **Python 3.10+**: Modern Python features and type hints
- **Streamlit**: Web UI framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Configuration and validation
- **Multiple AI Providers**: OpenAI, Anthropic, Google

---

## Architecture Patterns

### 1. Layered Architecture

The application follows a clean layered architecture:

```
UI Layer (Streamlit)
       ↓
Service Layer (AI Services)
       ↓
Repository Layer (Database Access)
       ↓
Data Layer (SQLAlchemy Models)
```

### 2. Repository Pattern

Database operations are abstracted through repositories:
- **ConversationRepository**: Handles all conversation and message CRUD operations
- **Benefits**: Testability, separation of concerns, easier to swap database implementations

### 3. Factory Pattern

The `AIServiceFactory` creates AI service instances:
```python
service = AIServiceFactory.create("openai", settings)
```

### 4. Strategy Pattern

Different AI providers implement the same `BaseAIService` interface:
```python
class BaseAIService(ABC):
    @abstractmethod
    def chat(self, messages, ...):
        pass
```

---

## Component Breakdown

### 1. Configuration Layer (`src/chatbot/config/`)

**Purpose**: Manage application settings and environment variables

**Key File**: `settings.py`
```python
class Settings(BaseSettings):
    openai_api_key: Optional[str]
    anthropic_api_key: Optional[str]
    # ... other settings
```

**How it works**:
1. Pydantic loads environment variables from `.env`
2. Validates types and values (e.g., temperature 0-2)
3. Provides typed access to configuration
4. Uses `@lru_cache` for performance

**Example**:
```python
from chatbot.config import get_settings

settings = get_settings()
api_key = settings.openai_api_key
```

---

### 2. Data Layer (`src/chatbot/models/`)

**Purpose**: Define database schema using SQLAlchemy ORM

**Key File**: `conversation.py`

**Models**:
- **Conversation**: Stores chat sessions
  - `id`, `title`, `provider`, `model`
  - `total_tokens`, `total_cost`
  - `created_at`, `updated_at`
  - Relationship: `messages`

- **Message**: Stores individual messages
  - `id`, `conversation_id`, `role`, `content`
  - `tokens`, `created_at`
  - Relationship: `conversation`

**How it works**:
```python
# SQLAlchemy creates tables automatically
Base.metadata.create_all(bind=engine)

# ORM allows Python object manipulation
conversation = Conversation(title="Chat", provider="openai")
session.add(conversation)
session.commit()
```

---

### 3. Repository Layer (`src/chatbot/repositories/`)

**Purpose**: Abstract database operations

**Key Files**:
- `database.py`: Database connection management
- `conversation_repository.py`: CRUD operations

**DatabaseManager**:
```python
class DatabaseManager:
    def initialize(self):
        # Create engine
        # Create session factory
        # Create tables

    def get_session(self):
        # Yield session with cleanup
```

**ConversationRepository**:
```python
class ConversationRepository:
    def create_conversation(self, title, provider, model):
        # Create and save conversation

    def add_message(self, conversation_id, role, content):
        # Add message to conversation

    def get_messages(self, conversation_id):
        # Retrieve all messages
```

**Benefits**:
- Single place for database logic
- Easy to mock for testing
- Transaction management
- Error handling

---

### 4. Service Layer (`src/chatbot/services/`)

**Purpose**: Integrate with AI providers

**Key Components**:

#### Base Service (`base.py`)
```python
class BaseAIService(ABC):
    @abstractmethod
    def chat(self, messages, model, temperature, max_tokens, stream):
        """Send chat request"""

    @abstractmethod
    def get_available_models(self):
        """List available models"""

    @abstractmethod
    def validate_api_key(self):
        """Check API key validity"""
```

#### OpenAI Service (`openai_service.py`)
```python
class OpenAIService(BaseAIService):
    def chat(self, messages, ...):
        # Count input tokens
        # Call OpenAI API
        # Extract response
        # Estimate cost
        # Return AIResponse
```

**AIResponse** (standardized response):
```python
@dataclass
class AIResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    metadata: Optional[Dict]
```

#### Factory (`ai_service_factory.py`)
```python
class AIServiceFactory:
    @staticmethod
    def create(provider: str, settings: Settings):
        if provider == "openai":
            return OpenAIService(settings.openai_api_key)
        elif provider == "anthropic":
            return AnthropicService(settings.anthropic_api_key)
        # ...
```

---

### 5. UI Layer (`src/chatbot/ui/`)

**Purpose**: Streamlit web interface

**Key File**: `app.py`

**Main Functions**:

1. **initialize_session_state()**
   - Sets up Streamlit session variables
   - Stores: messages, conversation_id, settings, statistics

2. **render_sidebar()**
   - Provider selection dropdown
   - Model selection dropdown
   - Advanced settings (temperature, max_tokens)
   - Conversation list with load/delete buttons
   - Session statistics

3. **render_chat()**
   - Display message history
   - Handle user input
   - Call AI service
   - Save to database
   - Update UI

**Flow**:
```
User enters message
  ↓
Add to session_state.messages
  ↓
Create AI service
  ↓
Call service.chat()
  ↓
Display response
  ↓
Save to database
  ↓
Update statistics
```

---

### 6. Utilities (`src/chatbot/utils/`)

#### Logger (`logger.py`)
```python
def setup_logger(name, log_level, log_file):
    # Create logger
    # Add console handler
    # Add file handler (if specified)
    # Set formatters
```

#### Token Counter (`token_counter.py`)
```python
def count_tokens(text, model):
    # Use tiktoken for OpenAI models
    # Fallback to character estimation

def estimate_cost(input_tokens, output_tokens, provider, model):
    # Look up pricing
    # Calculate cost
    # Return USD amount
```

**Pricing Data**:
```python
PRICING = {
    "openai": {
        "gpt-4": {"input": 0.03, "output": 0.06},
        # ... more models
    },
    # ... more providers
}
```

---

## Data Flow

### Sending a Message

1. **User Input** (UI Layer)
   ```python
   prompt = st.chat_input("Send a message...")
   ```

2. **Add to Session State** (UI Layer)
   ```python
   st.session_state.messages.append({
       "role": "user",
       "content": prompt
   })
   ```

3. **Create AI Service** (Service Layer)
   ```python
   service = AIServiceFactory.create(
       st.session_state.selected_provider,
       settings
   )
   ```

4. **Generate Response** (Service Layer)
   ```python
   response = service.chat(
       messages=st.session_state.messages,
       model=st.session_state.selected_model,
       temperature=st.session_state.temperature
   )
   ```

5. **Save to Database** (Repository Layer)
   ```python
   repo.add_message(
       conversation_id=...,
       role="user",
       content=prompt
   )
   repo.add_message(
       conversation_id=...,
       role="assistant",
       content=response.content
   )
   ```

6. **Update UI** (UI Layer)
   ```python
   st.session_state.messages.append({
       "role": "assistant",
       "content": response.content
   })
   st.session_state.total_tokens += response.total_tokens
   st.session_state.total_cost += response.cost
   ```

---

## Key Design Decisions

### 1. Why Pydantic for Configuration?
- **Type Safety**: Compile-time type checking
- **Validation**: Automatic validation of values
- **Documentation**: Self-documenting with Field descriptions
- **Environment Variables**: Automatic loading from .env

### 2. Why Repository Pattern?
- **Testability**: Easy to mock database operations
- **Flexibility**: Can swap database implementations
- **Centralization**: All DB logic in one place
- **Transaction Management**: Consistent error handling

### 3. Why Abstract Base Class for AI Services?
- **Consistency**: All providers have same interface
- **Extensibility**: Easy to add new providers
- **Type Safety**: IDE autocomplete and type checking
- **Documentation**: Clear contract for implementations

### 4. Why SQLite?
- **Simplicity**: No separate database server needed
- **Portability**: Single file database
- **Sufficient**: Handles chatbot use case well
- **Upgradeable**: Can migrate to PostgreSQL if needed

### 5. Why Streamlit?
- **Rapid Development**: Quick to build UIs
- **Python-Native**: No JavaScript needed
- **Built-in State Management**: Session state handling
- **Deployment**: Easy deployment options

---

## Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Example: Testing `count_tokens()` function

### Integration Tests
- Test component interactions
- Use in-memory SQLite database
- Example: Testing repository operations

### Test Coverage
- Aim for >80% coverage
- Focus on business logic
- Use `pytest-cov` for reporting

---

## Logging Strategy

### Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages

### What to Log
- API calls and responses
- Database operations
- Errors and exceptions
- User actions (conversation create/delete)

### Example
```python
logger.info(f"Created conversation: {conversation.id}")
logger.error(f"Failed to create conversation: {e}")
logger.debug(f"Sending request to OpenAI: model={model}")
```

---

## Future Improvements

1. **Caching**: Add Redis for caching responses
2. **Async**: Use async/await for better performance
3. **Streaming**: Implement streaming responses
4. **Authentication**: Add user authentication
5. **Rate Limiting**: Implement request rate limiting
6. **Metrics**: Add Prometheus metrics
7. **Monitoring**: Add error tracking (Sentry)

---

This explanation covers the core architecture and design patterns. For specific implementation details, refer to the source code with comprehensive docstrings and type hints.
