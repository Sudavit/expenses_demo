from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# 1. SQLAlchemy (The Database Table)
Base = declarative_base()


class UserDB(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


# 2. Pydantic (The Data Validation/API Schema)
class UserSchema(BaseModel):
    id: int
    name: str
    email: str
