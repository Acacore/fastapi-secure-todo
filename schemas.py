from pydantic import BaseModel
from typing import Optional, Annotated
import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from fastapi_users import schemas

class CreateUser(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    

class LoginUser(BaseModel):
    email: str
    password: str

class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True # Use this instead of orm_mode = True




class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserDelete(BaseModel):
    id: uuid.UUID


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

