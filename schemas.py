from pydantic import BaseModel
from typing import Optional, Annotated
import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class ToDoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ToDoRead(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class ToDoDelete(BaseModel):
    id: uuid.UUID

