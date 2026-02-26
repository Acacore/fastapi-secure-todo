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



# BASE SCHEMA (Shared fields) ---
class ToDoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False



# CREATE SCHEMA (What the user sends) ---
class ToDoCreate(ToDoBase):
    pass # In this case, it's the same as Base



# UPDATE SCHEMA (All fields optional for PATCH) ---
class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    # We don't include user_id here because a user shouldn't change ownership


# READ SCHEMA (What the API returns) ---
class ToDoRead(ToDoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True