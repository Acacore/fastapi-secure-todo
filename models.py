from sqlmodel import SQLModel, Field
from typing import Optional, Annotated
import uuid
from datetime import datetime, timezone


class ToDo(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
updated_at: datetime = Field(
default_factory=lambda: datetime.now(timezone.utc),
sa_onupdate=lambda: datetime.now(timezone.utc)
)
completed_at: Optional[datetime] = None