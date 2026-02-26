from sqlmodel import SQLModel, Field, Column, create_engine, Session, select, DateTime
from typing import Optional
import uuid
from datetime import datetime, timezone
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
# from sqlalchemy import DateTime


class User(SQLModelBaseUserDB, SQLModel, table=True):
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)


class ToDo(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: uuid.UUID = Field(foreign_key="user.id") # Ensure this is here!

    # Fix: Move these inside the class (Indent them)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            default=lambda: datetime.now(timezone.utc), 
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )
    
    completed_at: Optional[datetime] = None