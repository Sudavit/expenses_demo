from decimal import Decimal
from typing import Any

from expenses_demo.expenses import Category, Expense


# Placeholder to satisfy ty's "call-non-callable" check during RED phase
class _MissingAdapter:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError("Adapter not imported correctly")


try:
    from expenses_demo.adapters import DictExpenseRepository
except ImportError:
    DictExpenseRepository: Any = _MissingAdapter


def test_add_and_get():
    """Test adding an expense and retrieving it by ID."""
    # This assertion now serves as our explicit runtime check
    assert DictExpenseRepository is not _MissingAdapter, (
        "DictExpenseRepository not implemented"
    )

    repo = DictExpenseRepository()
    expense = Expense(amount=Decimal("5.50"), category=Category.FOOD, user_id=1)

    saved = repo.add(expense)
    assert saved.id is not None

    retrieved = repo.get(saved.id)
    assert retrieved is not None
    assert retrieved.amount == Decimal("5.50")
    assert retrieved is not saved


def test_list_all():
    """Test retrieving all expenses from the dict store."""
    # Ensure callability for ty
    assert DictExpenseRepository is not _MissingAdapter
    repo = DictExpenseRepository()

    repo.add(Expense(amount=Decimal("10.00"), category=Category.SOFTWARE, user_id=1))
    repo.add(Expense(amount=Decimal("20.00"), category=Category.TRAVEL, user_id=1))

    all_expenses = repo.list_all()
    assert len(all_expenses) == 2


def test_decimal_integrity():
    """Verify that the repository/model maintains Decimal via the internal validator."""
    assert DictExpenseRepository is not _MissingAdapter
    repo = DictExpenseRepository()

    # FIX: We use model_validate to create the instance.
    # This triggers the 'coerce_to_decimal' validator IMMEDIATELY,
    # ensuring the object is "clean" before it ever hits the repository.
    raw_data = {"amount": "99.99", "category": Category.SOFTWARE, "user_id": 1}
    expense = Expense.model_validate(raw_data)

    saved = repo.add(expense)
    assert saved.id is not None

    retrieved = repo.get(saved.id)
    assert retrieved is not None

    # Assertions remain identical
    assert isinstance(retrieved.amount, Decimal)
    assert retrieved.amount == Decimal("99.99")
