from typing import List, Optional, Sequence, Any, Union, cast
from enum import StrEnum, auto
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from decimal import Decimal
from pydantic import field_validator


class Category(StrEnum):
    FOOD = auto()
    SOFTWARE = auto()
    TRAVEL = auto()


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    # Relationship: One user has many expenses
    expenses: List["Expense"] = Relationship(back_populates="owner")


class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Update 1: Hint that we accept multiple types for 'amount'
    amount: Union[Decimal, float, str] = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2,
        sa_column_kwargs={"nullable": False},
    )

    category: Category

    # Update 2: Set a default of None so it's optional in the constructor,
    # but keep nullable=False so it's required in the database.
    user_id: int = Field(
        default=None, foreign_key="user.id", sa_column_kwargs={"nullable": False}
    )

    owner: User = Relationship(back_populates="expenses")

    @field_validator("amount", mode="before")
    @classmethod
    def coerce_to_decimal(cls, v: Any) -> Decimal:
        """Automatically convert strings or floats to Decimal."""
        if isinstance(v, Decimal):
            return v
        return Decimal(str(v))


class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, expense: Expense) -> Expense:
        self.session.add(expense)
        # We don't commit here; we let the "Unit of Work"
        # (the session owner) decide when to commit.
        return expense

    def get_by_user(self, user: User) -> Sequence[Expense]:
        if user.id is None:
            return []  # A non-persisted user cannot have expenses
        statement = select(Expense).where(Expense.user_id == user.id)
        return self.session.exec(statement).all()

    def get_all(self) -> Sequence[Expense]:
        return self.session.exec(select(Expense)).all()

    def add_all(self, expenses: list[Expense]) -> None:
        self.session.add_all(expenses)

    # Inside your ExpenseRepository:
    def total_for_user(self, user: User) -> Decimal:
        """Calculate the exact sum for a user's expenses."""
        expenses = self.get_by_user(user)
        # Cast the final result to Decimal to satisfy the Inspector
        total = sum((e.amount for e in expenses), Decimal("0.00"))
        return cast(Decimal, total)


# Database Setup
engine = create_engine("sqlite:///:memory:")  # In-memory for testing
SQLModel.metadata.create_all(engine)


def demo_relationship():
    with Session(engine) as session:
        # Initialize the Repository
        repo = ExpenseRepository(session)

        # 1. Create Data
        me = User(username="Galfridus")
        session.add(me)
        session.commit()  # Need the ID for the next step
        session.refresh(me)

        # 2. Use Repository to add an expense
        bill = Expense(amount=75.00, category=Category.TRAVEL, owner=me)
        repo.add(bill)
        session.commit()

        # 3. Use Repository to query
        my_expenses = repo.get_by_user(me)
        print(f"Found {len(my_expenses)} expenses for {me.username}")


if __name__ == "__main__":
    demo_relationship()
