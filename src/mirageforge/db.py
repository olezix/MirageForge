"""
Database connection and session management.

Provides database initialization, session factory, and utility functions
for working with SQLAlchemy in both sync and async contexts.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from mirageforge.config import get_settings
from mirageforge.models import Base


def get_engine(database_url: str | None = None) -> Engine:
    """
    Create SQLAlchemy engine.
    
    Args:
        database_url: Database URL. If None, uses settings.DATABASE_URL
        
    Returns:
        SQLAlchemy Engine instance
    """
    if database_url is None:
        database_url = get_settings().database_url
    
    # SQLite-specific options
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    
    engine = create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        echo=get_settings().debug and get_settings().app_env == "development",
    )
    return engine


def init_db(engine: Engine | None = None) -> None:
    """
    Initialize database by creating all tables.
    
    Args:
        engine: SQLAlchemy Engine. If None, creates new engine from settings.
    """
    if engine is None:
        engine = get_engine()
    
    Base.metadata.create_all(bind=engine)


def drop_db(engine: Engine | None = None) -> None:
    """
    Drop all database tables. Use with caution!
    
    Args:
        engine: SQLAlchemy Engine. If None, creates new engine from settings.
    """
    if engine is None:
        engine = get_engine()
    
    Base.metadata.drop_all(bind=engine)


def get_session_factory(engine: Engine | None = None) -> sessionmaker:
    """
    Create session factory.
    
    Args:
        engine: SQLAlchemy Engine. If None, creates new engine from settings.
        
    Returns:
        Session factory
    """
    if engine is None:
        engine = get_engine()
    
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Automatically commits on success, rolls back on exception,
    and closes the session.
    
    Yields:
        SQLAlchemy Session
    """
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db_session() -> Session:
    """
    Get a new database session.
    
    Caller is responsible for closing the session.
    
    Returns:
        SQLAlchemy Session
    """
    session_factory = get_session_factory()
    return session_factory()


# Global engine and session factory for reuse
_engine: Engine | None = None
_session_factory: sessionmaker | None = None


def get_global_engine() -> Engine:
    """Get or create global engine instance."""
    global _engine
    if _engine is None:
        _engine = get_engine()
    return _engine


def get_global_session_factory() -> sessionmaker:
    """Get or create global session factory."""
    global _session_factory
    if _session_factory is None:
        _session_factory = get_session_factory(get_global_engine())
    return _session_factory


@contextmanager
def get_db_global() -> Generator[Session, None, None]:
    """
    Context manager using global engine and session factory.
    
    More efficient than get_db() for repeated use.
    """
    session_factory = get_global_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def reset_global_connections() -> None:
    """Reset global engine and session factory (useful for testing)."""
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
