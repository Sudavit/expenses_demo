from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine


# --- The Model ---
class Agent(SQLModel, table=True):
    """A single class that is both a Pydantic model and a SQLAlchemy table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_identity: str
    power_level: int = 100


# --- The Database Engine ---
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_agent():
    # Validation happens here automatically (Pydantic behavior)
    new_agent = Agent(
        name="Galfridus", secret_identity="Python Architect", power_level=9001
    )

    with Session(engine) as session:
        session.add(new_agent)
        session.commit()
        session.refresh(new_agent)
        print(f"Created Agent: {new_agent.name} with ID: {new_agent.id}")


if __name__ == "__main__":
    create_db_and_tables()
    create_agent()
