"""
AAW Master Chatbot - Application Entry Point

This is the main entry point for running the Streamlit chatbot application.
Run with: streamlit run app.py
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from chatbot.ui.app import run_app

if __name__ == "__main__":
    run_app()
