import pytest
from sqlmodel import Session, SQLModel, create_engine

from expenses_demo.adapters import DictExpenseRepository
from expenses_demo.expenses import SQLExpenseRepository
from expenses_demo.factory import get_repository


@pytest.fixture
def sqlite_session():
    """Provides a transient SQLModel session and ensures engine cleanup."""
    # Use a unique name for the in-memory DB to avoid collisions if needed
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # FIX: Explicitly dispose the engine to close all connections
    engine.dispose()


def test_factory_returns_memory_repo():
    """Verify factory correctly instantiates the Goldfish store."""
    repo = get_repository("memory")
    assert isinstance(repo, DictExpenseRepository)


def test_factory_returns_sql_repo(sqlite_session):
    """Verify factory correctly instantiates the SQL Elephant."""
    repo = get_repository("sql", session=sqlite_session)
    assert isinstance(repo, SQLExpenseRepository)


def test_factory_requires_session_for_sql():
    """Verify the Kill-Switch for missing SQL sessions."""
    with pytest.raises(ValueError, match="SQL repository requires an active Session"):
        get_repository("sql", session=None)


def test_factory_invalid_type():
    with pytest.raises(ValueError, match="Unknown repository type"):
        get_repository("invalid")  # type: ignore
