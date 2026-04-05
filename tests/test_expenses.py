from sqlmodel import Session
from expenses_demo import User, Expense, Category, ExpenseRepository, demo_relationship
from decimal import Decimal


def test_repo_add_expense(session: Session):
    # Setup
    repo = ExpenseRepository(session)
    user = User(username="Galfridus")
    session.add(user)
    session.commit()

    # Action
    expense = Expense(amount=Decimal(42.0), category=Category.SOFTWARE, owner=user)
    repo.add(expense)
    session.commit()

    # Assert
    all_expenses = repo.get_all()
    assert len(all_expenses) == 1
    assert all_expenses[0].amount == 42.00
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
    e1 = Expense(amount=Decimal(10.00), category=Category.FOOD, owner=u1)
    e2 = Expense(amount=Decimal(20.00), category=Category.TRAVEL, owner=u2)
    repo.add(e1)
    repo.add(e2)
    session.commit()

    # Action
    u1_expenses = repo.get_by_user(u1)

    # Assert
    assert len(u1_expenses) == 1
    assert u1_expenses[0].amount == 10.00
    assert u1_expenses[0].user_id == u1.id


def test_category_enum_integrity(session: Session):
    # Verify that we are using the StrEnum correctly
    expense = Expense(amount=Decimal(5.00), category=Category.FOOD)
    assert expense.category == "food"
    assert isinstance(expense.category, Category)


def test_decimal_precision(session: Session):
    repo = ExpenseRepository(session)
    user = User(username="Galfridus")
    session.add(user)
    session.commit()

    # Always pass strings to Decimal to preserve precision
    e1 = Expense(amount=Decimal("10.10"), category=Category.FOOD, owner=user)
    e2 = Expense(amount=Decimal("20.20"), category=Category.FOOD, owner=user)

    repo.add(e1)
    repo.add(e2)
    session.commit()

    assert repo.total_for_user(user) == Decimal("30.30")


def test_total_for_user_accuracy(session: Session):
    repo = ExpenseRepository(session)
    user = User(username="Galfridus")
    session.add(user)
    session.commit()
    session.refresh(user)

    # 1. Test Empty Case
    assert repo.total_for_user(user) == Decimal("0.00")

    # 2. Test Multi-item Case with precision
    e1 = Expense(amount=Decimal(10.25), category=Category.FOOD, owner=user)
    e2 = Expense(amount=Decimal(20.50), category=Category.TRAVEL, owner=user)
    repo.add(e1)
    repo.add(e2)
    session.commit()

    assert repo.total_for_user(user) == Decimal("30.75")


def test_get_by_user_with_no_id(session: Session):
    repo = ExpenseRepository(session)
    unsaved_user = User(username="Ghost")
    # user.id is None here
    assert repo.get_by_user(unsaved_user) == []


def test_expense_amount_validation_error():
    # Approach: Use model_validate to force the coercion logic
    data = {"amount": "not-a-number", "category": Category.FOOD}
    e = Expense.model_validate(data)

    assert isinstance(e.amount, Decimal)
    assert e.amount == Decimal("0.00")


def test_main_demo_execution():
    """Executes the demo logic to ensure the 'main' path works."""
    # This covers the lines in the demo_relationship() function
    demo_relationship()
