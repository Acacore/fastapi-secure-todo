from sqlmodel import SQLModel, Field, Column
from typing import Optional
from sqlalchemy import DateTime
import uuid
from datetime import datetime, timezone



class ToDo(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    )
completed_at: Optional[datetime] = None
