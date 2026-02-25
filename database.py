from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Generator
from models import ToDo

# SQLite URL (simple file-based database)
DATABASE_URL = "sqlite:///./todo.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


# Function to create the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get a database session
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session