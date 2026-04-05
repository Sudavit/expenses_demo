from sqlmodel import Session
from sqlmodel_demo import User, Expense, Category, ExpenseRepository


def test_repo_add_expense(session: Session):
    # Setup
    repo = ExpenseRepository(session)
    user = User(username="Galfridus")
    session.add(user)
    session.commit()

    # Action
    expense = Expense(amount=42.0, category=Category.SOFTWARE, owner=user)
    repo.add(expense)
    session.commit()

    # Assert
    all_expenses = repo.get_all()
    assert len(all_expenses) == 1
    assert all_expenses[0].amount == 42.0
    assert all_expenses[0].owner.username == "Galfridus"


def test_get_by_user_filters_correctly(session: Session):
    repo = ExpenseRepository(session)

    # Create two users
    u1 = User(username="User1")
    u2 = User(username="User2")
    session.add_all([u1, u2])
    session.commit()
    session.refresh(u1)

    # Assign expense only to User1
    e1 = Expense(amount=10.0, category=Category.FOOD, owner=u1)
    e2 = Expense(amount=20.0, category=Category.TRAVEL, owner=u2)
    repo.add(e1)
    repo.add(e2)
    session.commit()

    # Action
    u1_expenses = repo.get_by_user(u1)

    # Assert
    assert len(u1_expenses) == 1
    assert u1_expenses[0].amount == 10.0
    assert u1_expenses[0].user_id == u1.id


def test_category_enum_integrity(session: Session):
    # Verify that we are using the StrEnum correctly
    expense = Expense(amount=5.0, category=Category.FOOD)
    assert expense.category == "food"
    assert isinstance(expense.category, Category)
