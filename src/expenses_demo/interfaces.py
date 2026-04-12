from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from expenses_demo.expenses import Expense


@runtime_checkable
class ExpenseRepository(Protocol):
    """The contract for expense persistence."""

    def add(self, expense: "Expense") -> "Expense": ...
    def get(self, expense_id: int) -> "Expense | None": ...
    def list_all(self) -> Sequence["Expense"]: ...
