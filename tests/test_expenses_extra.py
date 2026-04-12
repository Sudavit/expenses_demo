# tests/test_expenses_extra.py
from decimal import Decimal

from sqlmodel import Session

from expenses_demo import Category, Expense, SQLExpenseRepository, User


def test_sql_repo_get_and_list(session: Session):
    repo = SQLExpenseRepository(session)
    user = User(username="TestUser")
    session.add(user)
    session.commit()

    e1 = Expense(amount=Decimal("10.00"), category=Category.FOOD, owner=user)
    repo.add(e1)
    session.commit()

    # TYPE NARROWING: Tell ty that e1.id is definitely an int now.
    # Without this, ty sees 'int | None' and flags the next line.
    assert e1.id is not None

    # Exercises SQLExpenseRepository.get()
    retrieved = repo.get(e1.id)
    assert retrieved is not None
    assert retrieved.id == e1.id

    # Exercises SQLExpenseRepository.list_all()
    all_items = repo.list_all()
    assert len(all_items) == 1


def test_sql_repo_add_all(session: Session):
    repo = SQLExpenseRepository(session)
    user = User(username="BulkUser")
    session.add(user)
    session.commit()

    expenses = [
        Expense(amount=Decimal("1.00"), category=Category.FOOD, owner=user),
        Expense(amount=Decimal("2.00"), category=Category.TRAVEL, owner=user),
    ]

    # Exercises SQLExpenseRepository.add_all()
    repo.add_all(expenses)
    session.commit()

    assert len(repo.get_all()) == 2
