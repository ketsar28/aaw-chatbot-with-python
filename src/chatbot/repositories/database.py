"""
Database connection and session management.

This module handles database initialization and session management
using SQLAlchemy.
"""

import os
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from ..models.conversation import Base
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self, database_url: str):
        """
        Initialize database manager.

        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None

    def initialize(self) -> None:
        """Initialize database engine and create tables."""
        try:
            # Create data directory if using SQLite
            if self.database_url.startswith("sqlite"):
                db_path = self.database_url.replace("sqlite:///", "")
                db_dir = Path(db_path).parent
                db_dir.mkdir(parents=True, exist_ok=True)

            # Create engine
            if "sqlite" in self.database_url:
                # SQLite-specific configuration
                self.engine = create_engine(
                    self.database_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool,
                )
            else:
                self.engine = create_engine(self.database_url)

            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            # Create all tables
            Base.metadata.create_all(bind=self.engine)

            logger.info(f"Database initialized successfully: {self.database_url}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session.

        Yields:
            Database session
        """
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def close(self) -> None:
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


# Global database manager instance
_db_manager: DatabaseManager = None


def get_db() -> DatabaseManager:
    """
    Get global database manager instance.

    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        from ..config.settings import get_settings
        settings = get_settings()
        _db_manager = DatabaseManager(settings.database_url)
        _db_manager.initialize()
    return _db_manager
