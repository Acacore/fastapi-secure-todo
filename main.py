import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from database import get_session
from sqlmodel import select
from datetime import datetime, timezone
# Import local modules
from database import create_db_and_tables
from models import User, ToDo
from schemas import UserRead, CreateUser, UserUpdate, ToDoCreate, ToDoRead, ToDoUpdate
from sqlmodel import Session
from users import fastapi_users, auth_backend, get_user_manager
from fastapi.middleware.cors import CORSMiddleware

# LIFESPAN (Modern way to handle startup/shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    create_db_and_tables()
    yield
    # Logic here runs when the server stops (if needed)

# APP INITIALIZATION
app = FastAPI(
    title="To-Do List API",
    description="A secure API for managing tasks with JWT authentication.",
    version="1.0.0",
    lifespan=lifespan
)

# AUTHENTICATION ROUTES
# Provides: /auth/jwt/login and /auth/jwt/logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRATION ROUTE
# Provides: /auth/register
app.include_router(
    fastapi_users.get_register_router(UserRead, CreateUser),
    prefix="/auth",
    tags=["auth"],
)

# PASSWORD RESET ROUTE
# Provides: /auth/forgot-password and /auth/reset-password
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# USER MANAGEMENT ROUTE
# Provides: /users/me (GET, PATCH, DELETE)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# EXAMPLE PROTECTED ROUTE
# This dependency ensures only logged-in users can access a route
current_active_user = fastapi_users.current_user(active=True)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.first_name} {user.last_name}, you are logged in!"}


@app.post("/todos/", response_model=ToDoRead, status_code=201)
async def create_todo(
    todo_in: ToDoCreate, 
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    # Map Pydantic data to SQLModel and link the authenticated user
    new_todo = ToDo(**todo_in.model_dump(), user_id=user.id)
    
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


# GET ALL: Returns only the tasks belonging to the current user
@app.get("/todos/", response_model=list[ToDoRead])
async def read_todos(
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    # We filter by user_id so users can't see each other's lists
    statement = select(ToDo).where(ToDo.user_id == user.id)
    results = session.exec(statement)
    return results.all()

# GET ONE: Fetch a specific task by ID
@app.get("/todos/{todo_id}", response_model=ToDoRead)
async def read_todo_by_id(
    todo_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    db_todo = session.get(ToDo, todo_id)
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
        
    # Security: Ensure the user owns this specific To-Do
    if db_todo.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: uuid.UUID,
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    # 1. Fetch the task
    db_todo = session.get(ToDo, todo_id)
    
    # 2. If it doesn't exist, tell the user 404
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="To-Do not found"
        )

    # 3. SECURITY: Check if the user is the owner
    if db_todo.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to delete this task"
        )

    # 4. Remove from database
    session.delete(db_todo)
    session.commit()
    
    # Return nothing (204 No Content is the standard for successful deletion)
    return None


@app.patch("/todos/{todo_id}", response_model=ToDoRead)
async def update_todo(
    todo_id: uuid.UUID,
    todo_update: ToDoUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    # 1. Verify existence
    db_todo = session.get(ToDo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="To-Do not found")

    # 2. Verify ownership
    if db_todo.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this task")

    # 3. Partial Update logic
    update_data = todo_update.model_dump(exclude_unset=True)
    
    # Auto-handle the completed_at timestamp
    if "completed" in update_data:
        if update_data["completed"] and not db_todo.completed:
            db_todo.completed_at = datetime.now(timezone.utc)
        elif not update_data["completed"]:
            db_todo.completed_at = None

    db_todo.sqlmodel_update(update_data)
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo