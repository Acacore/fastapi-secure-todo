import uuid
import os
from typing import Optional
from fastapi import Depends, Request # Removed duplicate Request
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers
from dotenv import load_dotenv
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport    

from database import get_user_db 
from models import User    

load_dotenv()
SECRET = os.getenv("JWT_SECRET_KEY", "DEVELOPMENT_FALLBACK_SECRET")

# 1. Transport & Strategy
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# 2. The Backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# 3. The Manager
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# 4. The Main FastAPI Users Object (The "Glue")
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)