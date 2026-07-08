"""
schemas/user.py
---------------
Pydantic request and response models for user authentication.

Design decisions:
  - Passwords are NEVER returned in any response schema.
  - Role is validated at the schema level using Literal so invalid roles
    are rejected before touching any business logic or the database.
  - LoginResponse and RegisterResponse bundle the JWT + user profile in
    a single payload so the frontend avoids a follow-up /me call.
"""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Request schemas (inbound data from client)
# ---------------------------------------------------------------------------

class UserRegister(BaseModel):
    """Payload for POST /auth/register."""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100, examples=["Jane Smith"])
    password: str = Field(..., min_length=6, max_length=100)
    # Literal enforces the only two valid roles at the schema layer.
    role: Literal["member", "manager"] = "member"


class UserLogin(BaseModel):
    """Payload for POST /auth/login."""
    email: EmailStr
    password: str = Field(..., min_length=1)


# ---------------------------------------------------------------------------
# Response schemas (outbound data to client)
# ---------------------------------------------------------------------------

class UserOut(BaseModel):
    """
    Safe public representation of a user.
    password_hash is intentionally excluded from this schema.
    """
    id: str
    email: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows constructing from SQLAlchemy ORM objects


class Token(BaseModel):
    """Bare token response — used when only the token itself is needed."""
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """
    Full authentication response returned by both /login and /register.
    Bundles the JWT access token with the user's profile so the client
    can store both in a single round trip.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# Alias so router code can use a semantically accurate name on each endpoint
RegisterResponse = LoginResponse
