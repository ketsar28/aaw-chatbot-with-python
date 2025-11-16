# 🤖 AAW Master Chatbot

[![CI/CD Pipeline](https://github.com/ketsar28/aaw-chatbot-with-python/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/ketsar28/aaw-chatbot-with-python/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A **production-ready, multi-provider AI chatbot** built with Python, featuring support for OpenAI GPT, Anthropic Claude, and Google Gemini models. This master-level project demonstrates best practices in software architecture, testing, deployment, and documentation.

**Developed by:** [Ketsar Ali](https://github.com/ketsar28)

---

## 👨‍💻 About the Author

<div align="center">

### Ketsar Ali

**AI Engineer & Full-Stack Developer**

[![GitHub](https://img.shields.io/badge/GitHub-ketsar28-181717?style=for-the-badge&logo=github)](https://github.com/ketsar28/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ketsar_Ali-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ketsarali/)
[![Instagram](https://img.shields.io/badge/Instagram-ketsar.aaw-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/ketsar.aaw/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-ketsar-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/ketsar)
[![Streamlit](https://img.shields.io/badge/Streamlit-ketsar28-FF4B4B?style=for-the-badge&logo=streamlit)](https://share.streamlit.io/user/ketsar28)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Contact_Me-25D366?style=for-the-badge&logo=whatsapp)](https://api.whatsapp.com/send/?phone=6285155343380&text=Hi%20Ketsar,%20I'm%20interested%20in%20your%20AAW%20Chatbot%20project!)

</div>

Passionate about building innovative AI solutions and creating production-ready applications. This chatbot project showcases enterprise-level software engineering practices combined with cutting-edge AI technology.

---

## ✨ Features

### 🎯 Core Features
- **Multi-Provider Support**: Seamlessly switch between OpenAI (GPT-4, GPT-3.5), Anthropic (Claude 3), and Google (Gemini)
- **Conversation Persistence**: SQLite database for saving and loading conversation history
- **Cost Tracking**: Real-time token usage and cost estimation for all providers
- **Responsive UI**: Clean, modern Streamlit interface with chat bubbles and settings panel
- **Model Selection**: Choose from multiple models within each provider
- **Advanced Settings**: Adjustable temperature, max tokens, and other parameters

### 🏗️ Architecture Features
- **Modular Design**: Clean separation of concerns with services, repositories, and models
- **Type Safety**: Comprehensive type hints using Pydantic
- **Error Handling**: Robust error handling and logging throughout
- **Configuration Management**: Environment-based configuration with validation
- **Database Layer**: SQLAlchemy ORM with repository pattern
- **Service Abstraction**: Common interface for all AI providers

### 🚀 Production Features
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Code Quality**: Linting with flake8, formatting with black and isort
- **Logging**: Structured logging with file and console outputs
- **Health Checks**: Docker health checks for monitoring

---

## 📋 Table of Contents

- [About the Author](#-about-the-author)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage](#-usage)
- [Architecture](#%EF%B8%8F-architecture)
- [Development](#%EF%B8%8F-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [API Providers Setup](#-api-providers-setup)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Connect With Me](#-connect-with-me)
- [License](#-license)

---

## 🔧 Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Docker** (optional, for containerized deployment)
- At least one API key from:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic](https://console.anthropic.com/)
  - [Google AI](https://makersuite.google.com/app/apikey)

---

## 📦 Installation

### Method 1: Standard Installation

1. **Clone the repository**
```bash
git clone https://github.com/ketsar28/aaw-chatbot-with-python.git
cd aaw-chatbot-with-python
```

2. **Create a virtual environment** (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

### Method 2: Docker Installation

1. **Clone the repository**
```bash
git clone https://github.com/ketsar28/aaw-chatbot-with-python.git
cd aaw-chatbot-with-python
```

2. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

---

## 🚀 Quick Start

### Running Locally

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Running with Docker

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required: At least one AI provider API key
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-api-key-here

# Application Settings
APP_NAME=AAW Master Chatbot
APP_VERSION=2.0.0
ENVIRONMENT=production

# Database
DATABASE_URL=sqlite:///./data/chatbot.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/chatbot.log

# AI Settings
DEFAULT_AI_PROVIDER=openai
DEFAULT_MODEL=gpt-4
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Optional* |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | Optional* |
| `GOOGLE_API_KEY` | Google API key | - | Optional* |
| `DEFAULT_AI_PROVIDER` | Default provider (openai/anthropic/google) | openai | No |
| `DEFAULT_MODEL` | Default model name | gpt-4 | No |
| `TEMPERATURE` | Model temperature (0-2) | 0.7 | No |
| `MAX_TOKENS` | Max tokens per response | 4096 | No |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO | No |

*At least one provider API key is required

---

## 💡 Usage

### Basic Usage

1. **Start the Application**
   - Run `streamlit run app.py`
   - Open browser at `http://localhost:8501`

2. **Select AI Provider**
   - Use the sidebar to choose between OpenAI, Anthropic, or Google
   - Select your preferred model

3. **Start Chatting**
   - Type your message in the chat input
   - Press Enter to send
   - View AI response in real-time

### Advanced Features

#### Conversation Management
- **New Conversation**: Click "➕ New Conversation" in sidebar
- **Load Conversation**: Click on any saved conversation to resume
- **Delete Conversation**: Click the 🗑️ button next to a conversation

#### Settings Adjustment
- **Temperature**: Control randomness (0 = focused, 2 = creative)
- **Max Tokens**: Set maximum response length
- **Provider/Model**: Switch between different AI providers and models

#### Cost Tracking
- View real-time token usage in the sidebar
- Monitor estimated costs per conversation
- Track total spending across all conversations

---

## 🏗️ Architecture

### Project Structure

```
aaw-chatbot-with-python/
├── src/
│   └── chatbot/
│       ├── config/           # Configuration management
│       │   ├── __init__.py
│       │   └── settings.py   # Pydantic settings
│       ├── models/           # Database models
│       │   ├── __init__.py
│       │   └── conversation.py
│       ├── repositories/     # Database access layer
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── conversation_repository.py
│       ├── services/         # AI provider services
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── openai_service.py
│       │   ├── anthropic_service.py
│       │   ├── google_service.py
│       │   └── ai_service_factory.py
│       ├── ui/              # Streamlit UI
│       │   ├── __init__.py
│       │   └── app.py
│       └── utils/           # Utilities
│           ├── __init__.py
│           ├── logger.py
│           └── token_counter.py
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                   # Documentation
├── .github/                # GitHub Actions
│   └── workflows/
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── pytest.ini             # Pytest configuration
├── .env.example           # Example environment file
└── README.md              # This file
```

### Component Overview

#### 1. **Configuration Layer** (`config/`)
- Manages application settings using Pydantic
- Loads and validates environment variables
- Provides typed configuration objects

#### 2. **Data Layer** (`models/`, `repositories/`)
- SQLAlchemy ORM models for conversations and messages
- Repository pattern for database operations
- Clean separation of data access logic

#### 3. **Service Layer** (`services/`)
- Abstract base class for AI providers
- Concrete implementations for OpenAI, Anthropic, and Google
- Factory pattern for service creation
- Unified response format across providers

#### 4. **UI Layer** (`ui/`)
- Streamlit-based web interface
- Session state management
- Real-time chat interface
- Settings and conversation management

#### 5. **Utilities** (`utils/`)
- Logging configuration
- Token counting and cost estimation
- Helper functions

---

## 🛠️ Development

### Setting Up Development Environment

1. **Clone and install**
```bash
git clone https://github.com/ketsar28/aaw-chatbot-with-python.git
cd aaw-chatbot-with-python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Install development tools**
```bash
pip install black isort flake8 mypy pytest pytest-cov
```

3. **Set up pre-commit hooks** (optional)
```bash
pip install pre-commit
pre-commit install
```

### Code Style

This project follows PEP 8 and uses:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/ --max-line-length=100

# Type check
mypy src/
```

### Adding a New AI Provider

1. Create a new service in `src/chatbot/services/`:

```python
from .base import BaseAIService, AIResponse

class NewProviderService(BaseAIService):
    def chat(self, messages, model=None, temperature=0.7, max_tokens=4096, stream=False):
        # Implementation
        pass

    def get_available_models(self):
        return ["model-1", "model-2"]

    def validate_api_key(self):
        # Validation logic
        pass
```

2. Update `AIServiceFactory` in `ai_service_factory.py`
3. Add configuration in `settings.py`
4. Update UI in `app.py`

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/chatbot --cov-report=html

# Run specific test file
pytest tests/unit/test_config.py

# Run with verbose output
pytest -v
```

### Test Structure

- **Unit Tests** (`tests/unit/`): Test individual components in isolation
- **Integration Tests** (`tests/integration/`): Test component interactions
- **Coverage**: Aim for >80% code coverage

### Writing Tests

Example test:

```python
def test_create_conversation(db_session):
    """Test creating a conversation."""
    repo = ConversationRepository(db_session)

    conversation = repo.create_conversation(
        title="Test",
        provider="openai",
        model="gpt-4"
    )

    assert conversation.id is not None
    assert conversation.title == "Test"
```

---

## 🚢 Deployment

### Docker Deployment

1. **Build the image**
```bash
docker build -t aaw-master-chatbot .
```

2. **Run the container**
```bash
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --name chatbot \
  aaw-master-chatbot
```

3. **Using Docker Compose** (recommended)
```bash
docker-compose up -d
```

### Cloud Deployment

#### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set environment variables in Streamlit Cloud dashboard
5. Deploy!

#### Deploying to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create aaw-master-chatbot

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key

# Deploy
git push heroku main

# Open app
heroku open
```

#### Deploying to AWS/GCP/Azure

See `docs/DEPLOYMENT.md` for detailed cloud deployment guides.

---

## 🔑 API Providers Setup

### OpenAI Setup

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Pricing**: Pay-as-you-go
- GPT-4: $0.03/1K input tokens, $0.06/1K output tokens
- GPT-3.5-turbo: $0.0005/1K input, $0.0015/1K output

### Anthropic Setup

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an account
3. Generate an API key
4. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Pricing**:
- Claude 3 Opus: $0.015/1K input, $0.075/1K output
- Claude 3 Sonnet: $0.003/1K input, $0.015/1K output
- Claude 3 Haiku: $0.00025/1K input, $0.00125/1K output

### Google Gemini Setup

1. Go to [makersuite.google.com](https://makersuite.google.com)
2. Sign in with Google account
3. Get API key
4. Add to `.env`: `GOOGLE_API_KEY=...`

**Pricing**: Free tier available
- Gemini Pro: $0.00025/1K input, $0.0005/1K output

---

## 🔍 Troubleshooting

### Common Issues

#### Issue: "No AI providers configured"
**Solution**: Add at least one API key to your `.env` file

#### Issue: "Database locked" error
**Solution**: Close other instances of the app or delete the database file

#### Issue: "Module not found" errors
**Solution**: Ensure you've installed all requirements and activated your virtual environment
```bash
pip install -r requirements.txt
```

#### Issue: Docker container won't start
**Solution**: Check logs for details
```bash
docker-compose logs
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/ketsar28/aaw-chatbot-with-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ketsar28/aaw-chatbot-with-python/discussions)
- **Direct Contact**: [WhatsApp Me](https://api.whatsapp.com/send/?phone=6285155343380&text=Hi%20Ketsar,%20I%20need%20help%20with%20AAW%20Chatbot!)

---

## 📚 Additional Documentation

- [Code Explanation](docs/CODE_EXPLANATION.md) - Detailed architecture and code walkthrough
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to this project

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/ketsar28/aaw-chatbot-with-python/issues).

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🌐 Connect With Me

I'm always excited to connect with fellow developers, AI enthusiasts, and potential collaborators!

<div align="center">

### Ketsar Ali

**AI Engineer | Full-Stack Developer | Tech Enthusiast**

[![GitHub](https://img.shields.io/badge/GitHub-Follow_Me-181717?style=for-the-badge&logo=github)](https://github.com/ketsar28/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ketsarali/)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/ketsar.aaw/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Profile-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/ketsar)
[![Streamlit](https://img.shields.io/badge/Streamlit-Apps-FF4B4B?style=for-the-badge&logo=streamlit)](https://share.streamlit.io/user/ketsar28)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat-25D366?style=for-the-badge&logo=whatsapp)](https://api.whatsapp.com/send/?phone=6285155343380&text=Hi%20Ketsar,%20I'm%20interested%20in%20collaborating!)

**📧 Let's build something amazing together!**

</div>

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/ketsar28/aaw-chatbot-with-python?style=social)
![GitHub forks](https://img.shields.io/github/forks/ketsar28/aaw-chatbot-with-python?style=social)
![GitHub issues](https://img.shields.io/github/issues/ketsar28/aaw-chatbot-with-python)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ketsar28/aaw-chatbot-with-python)

---

## 🗺️ Roadmap

- [ ] Add streaming responses for real-time chat
- [ ] Implement user authentication system
- [ ] Add conversation export (PDF, Markdown, JSON)
- [ ] Support for image inputs (GPT-4 Vision, Gemini Pro Vision)
- [ ] Voice input/output capabilities
- [ ] Custom system prompts per conversation
- [ ] Multi-language interface support
- [ ] Advanced analytics and usage dashboard
- [ ] Plugin system for extensibility
- [ ] Mobile-responsive PWA version

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2024 [Ketsar Ali](https://github.com/ketsar28). All rights reserved.**

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) for the incredible UI framework
- [OpenAI](https://openai.com) for GPT models and API
- [Anthropic](https://anthropic.com) for Claude models
- [Google](https://ai.google.dev) for Gemini models
- The open-source community for amazing tools and libraries

---

## 💖 Support This Project

If you find this project helpful, please consider:

- ⭐ **Starring** this repository
- 🐛 **Reporting bugs** and suggesting features
- 🔀 **Contributing** code improvements
- 📢 **Sharing** with others who might find it useful
- ☕ **Connecting** with me on social media

---

<div align="center">

### ⚡ Built with passion by [Ketsar Ali](https://github.com/ketsar28)

**Making AI accessible, one chat at a time** 🤖✨

[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)](https://github.com/ketsar28)
[![Built with Python](https://img.shields.io/badge/Built%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by AI](https://img.shields.io/badge/Powered%20by-AI-00D9FF?style=for-the-badge)](https://github.com/ketsar28/aaw-chatbot-with-python)

**⭐ Don't forget to star this repository if you found it helpful! ⭐**

</div>
