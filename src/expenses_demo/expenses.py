from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from enum import StrEnum, auto
from typing import Any

from pydantic import field_validator
from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    create_engine,
    select,
)

from expenses_demo.interfaces import ExpenseRepository as IExpenseRepository


class Category(StrEnum):
    FOOD = auto()
    SOFTWARE = auto()
    TRAVEL = auto()


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    # Relationship: One user has many expenses
    expenses: list["Expense"] = Relationship(back_populates="owner")


class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Update 1: Hint that we accept multiple types for 'amount'
    amount: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2,
        sa_column_kwargs={"nullable": False},
    )

    category: Category

    user_id: int = Field(
        default=None, foreign_key="user.id", sa_column_kwargs={"nullable": False}
    )

    owner: User = Relationship(back_populates="expenses")

    # Inside Expense class
    @field_validator("amount", mode="before")
    @classmethod
    def coerce_to_decimal(cls, v: Any) -> Decimal:
        """The 'Inspector' ensures data integrity before assignment."""
        if isinstance(v, Decimal):
            return v
        try:
            # If it's a float or string, cast it to string then Decimal
            return Decimal(str(v))
        except (ValueError, TypeError, InvalidOperation):
            # The 'Kill-Switch' for bad data: return a safe baseline
            return Decimal("0.00")


class SQLExpenseRepository(
    IExpenseRepository
):  # Renamed and marked as implementing Protocol
    def __init__(self, session: Session):
        self.session = session

    def add(self, expense: "Expense") -> "Expense":
        self.session.add(expense)
        # We don't commit here; we let the "Unit of Work"
        # (the session owner) decide when to commit.
        return expense

    def get(self, expense_id: int) -> "Expense | None":
        """Retrieve by ID to match Protocol signature."""
        return self.session.get(Expense, expense_id)

    # Matching the Protocol's list_all requirement
    def list_all(self) -> Sequence["Expense"]:
        return self.get_all()

    def get_by_user(self, user: User) -> Sequence["Expense"]:
        if user.id is None:
            return []  # A non-persisted user cannot have expenses
        statement = select(Expense).where(Expense.user_id == user.id)
        return self.session.exec(statement).all()

    def get_all(self) -> Sequence["Expense"]:
        return self.session.exec(select(Expense)).all()

    def add_all(self, expenses: list["Expense"]) -> None:
        self.session.add_all(expenses)

    # Inside your ExpenseRepository:
    def total_for_user(self, user: User) -> Decimal:
        """Calculate the exact sum for a user's expenses."""
        expenses = self.get_by_user(user)
        # Cast the final result to Decimal to satisfy the Inspector
        total = sum((e.amount for e in expenses), Decimal("0.00"))
        return total


# Database Setup
engine = create_engine("sqlite:///:memory:")  # In-memory for testing
SQLModel.metadata.create_all(engine)


def demo_relationship():
    with Session(engine) as session:
        # Initialize the Repository
        repo = SQLExpenseRepository(session)

        # 1. Create Data
        me = User(username="Galfridus")
        session.add(me)
        session.commit()  # Need the ID for the next step
        session.refresh(me)

        # 2. Use Repository to add an expense
        bill = Expense(amount=75.00, category=Category.TRAVEL, owner=me)  # type: ignore
        repo.add(bill)
        session.commit()

        # 3. Use Repository to query
        my_expenses = repo.get_by_user(me)
        print(f"Found {len(my_expenses)} expenses for {me.username}")


def main():
    demo_relationship()  # pragma: no cover


if __name__ == "__main__":
    main()
