from typing import List, Optional, Sequence
from enum import StrEnum, auto
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


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
    amount: float
    category: Category  # Uses our StrEnum

    # Foreign Key linking to User
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Relationship: Each expense belongs to one owner
    owner: User = Relationship(back_populates="expenses")


class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, expense: Expense) -> Expense:
        self.session.add(expense)
        # We don't commit here; we let the "Unit of Work"
        # (the session owner) decide when to commit.
        return expense

    def get_by_user(self, user: User) -> Sequence[Expense]:
        # Use the relationship or the ID safely
        statement = select(Expense).where(Expense.user_id == user.id)
        return self.session.exec(statement).all()

    def get_all(self) -> Sequence[Expense]:
        return self.session.exec(select(Expense)).all()


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
        bill = Expense(amount=75.0, category=Category.TRAVEL, owner=me)
        repo.add(bill)
        session.commit()

        # 3. Use Repository to query
        my_expenses = repo.get_by_user(me)
        print(f"Found {len(my_expenses)} expenses for {me.username}")


if __name__ == "__main__":
    demo_relationship()
