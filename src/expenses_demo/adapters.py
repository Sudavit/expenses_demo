# --- REFACTORED ADAPTER (src/expenses_demo/adapters.py) ---
import copy
from collections.abc import Sequence

from expenses_demo.expenses import Expense
from expenses_demo.interfaces import ExpenseRepository


class DictExpenseRepository(ExpenseRepository):
    """
    A dictionary-backed store.
    NOTE: Sequential ID generation here is for test-predictability only.
    The SQLExpenseRepository remains the 'Source of Truth' for ID logic.
    """

    def __init__(self) -> None:
        self._storage: dict[int, Expense] = {}
        self._next_id: int = 1

    def add(self, expense: Expense) -> Expense:
        """
        Adds an expense and returns a validated deep copy.
        We use model_validate to trigger the 'coerce_to_decimal' logic.
        """
        # Trigger validation/coercion by rebuilding from dict
        # This ensures 'amount' becomes a Decimal if it was a string
        validated_data = expense.model_dump()
        cloned = Expense.model_validate(validated_data)

        if cloned.id is None:
            cloned.id = self._next_id
            self._next_id += 1

        self._storage[cloned.id] = cloned
        return copy.deepcopy(cloned)

    def get(self, expense_id: int) -> Expense | None:
        item = self._storage.get(expense_id)
        return copy.deepcopy(item) if item is not None else None

    def list_all(self) -> Sequence[Expense]:
        return [copy.deepcopy(e) for e in self._storage.values()]
