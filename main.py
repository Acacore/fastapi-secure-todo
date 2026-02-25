import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

# Import local modules
from database import create_db_and_tables
from models import User
from schemas import UserRead, CreateUser, UserUpdate
from users import fastapi_users, auth_backend, get_user_manager

# 1. LIFESPAN (Modern way to handle startup/shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    create_db_and_tables()
    yield
    # Logic here runs when the server stops (if needed)

# 2. APP INITIALIZATION
app = FastAPI(
    title="To-Do List API",
    description="A secure API for managing tasks with JWT authentication.",
    version="1.0.0",
    lifespan=lifespan
)

# 3. AUTHENTICATION ROUTES
# Provides: /auth/jwt/login and /auth/jwt/logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# 4. REGISTRATION ROUTE
# Provides: /auth/register
app.include_router(
    fastapi_users.get_register_router(UserRead, CreateUser),
    prefix="/auth",
    tags=["auth"],
)

# 5. PASSWORD RESET ROUTE
# Provides: /auth/forgot-password and /auth/reset-password
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# 6. USER MANAGEMENT ROUTE
# Provides: /users/me (GET, PATCH, DELETE)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# 7. EXAMPLE PROTECTED ROUTE
# This dependency ensures only logged-in users can access a route
current_active_user = fastapi_users.current_user(active=True)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.first_name} {user.last_name}, you are logged in!"}

