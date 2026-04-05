from typing import List, Optional
from enum import StrEnum, auto
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


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


# Database Setup
engine = create_engine("sqlite:///:memory:")  # In-memory for testing
SQLModel.metadata.create_all(engine)


def demo_relationship():
    with Session(engine) as session:
        # Create a User
        me = User(username="Galfridus")

        # Create an Expense linked to that User
        api_bill = Expense(amount=50.0, category=Category.SOFTWARE, owner=me)

        session.add(me)
        session.commit()
        session.refresh(me)

        print(f"User: {me.username} {me.id}")
        print(f"Expenses: {[e.category for e in me.expenses]}")
        print(f"Billed: {api_bill.amount}")


if __name__ == "__main__":
    demo_relationship()
