from typing import Literal

from sqlmodel import Session

from expenses_demo.adapters import DictExpenseRepository
from expenses_demo.expenses import SQLExpenseRepository
from expenses_demo.interfaces import ExpenseRepository as IExpenseRepository

RepoType = Literal["memory", "sql"]


def get_repository(
    repo_type: Literal["memory", "sql"], session: Session | None = None
) -> IExpenseRepository:
    """
    Factory to select the repository implementation.

    Args:
        repo_type: Either 'memory' or 'sql'.
        session: Required for 'sql' type; ignored for 'memory'.

    Returns:
        An object conforming to the ExpenseRepository Protocol.
    """
    if repo_type == "memory":
        return DictExpenseRepository()

    if repo_type == "sql":
        if session is None:
            raise ValueError("SQL repository requires an active Session.")
        return SQLExpenseRepository(session)

    raise ValueError(f"Unknown repository type: {repo_type}")
