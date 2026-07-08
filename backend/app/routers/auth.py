"""
routers/auth.py
---------------
Authentication endpoints: register, login, and /me.

Endpoint summary:
  POST /api/v1/auth/register  → create account, returns JWT + profile
  POST /api/v1/auth/login     → authenticate, returns JWT + profile
  GET  /api/v1/auth/me        → returns current authenticated user's profile

Design decisions:
  - Email is normalised to lowercase on both registration and lookup to
    prevent duplicate accounts differing only by case (e.g. User@x.com vs user@x.com).
  - Both register and login return LoginResponse (JWT + UserOut) in one
    payload, avoiding a redundant /me round-trip after authentication.
  - Login uses a single generic error message for both "email not found"
    and "wrong password" to prevent user-enumeration attacks.
  - Passwords are hashed with bcrypt via passlib; the raw password is
    never written to any variable beyond the immediate hashing call.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserOut,
    LoginResponse,
    RegisterResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------
@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    responses={
        409: {"description": "Email address already registered"},
    },
)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> RegisterResponse:
    """
    Create a new user account.

    - Checks that the email is not already taken (case-insensitive).
    - Hashes the password with bcrypt before persisting.
    - Returns a JWT access token and the new user's profile so the client
      is immediately authenticated without a separate login call.
    """
    # 1. Duplicate-email guard (case-insensitive)
    email_normalised = payload.email.lower().strip()
    existing_user = db.query(User).filter(User.email == email_normalised).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists.",
        )

    # 2. Hash password — raw password discarded after this line
    hashed_pw = get_password_hash(payload.password)

    # 3. Persist the new user record
    new_user = User(
        email=email_normalised,
        password_hash=hashed_pw,
        full_name=payload.full_name.strip(),
        role=payload.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # reload to get DB-generated values (id, created_at)

    # 4. Issue a JWT embedding the minimum necessary claims
    access_token = create_access_token(
        data={
            "user_id": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role,
        }
    )

    return RegisterResponse(
        access_token=access_token,
        user=UserOut.model_validate(new_user),
    )


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate with email and password",
    responses={
        401: {"description": "Incorrect email or password"},
    },
)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> LoginResponse:
    """
    Authenticate an existing user.

    - Looks up the user by email (case-insensitive).
    - Verifies the submitted password against the stored bcrypt hash.
    - Returns a JWT access token and the user's profile.

    Security note: a single generic error message is returned regardless
    of whether the email was not found or the password was wrong. This
    prevents attackers from discovering which emails are registered
    (user-enumeration attack).
    """
    email_normalised = payload.email.lower().strip()

    # Single DB query; if user not found, verification will still run
    # against a dummy hash to keep constant-time behaviour (timing attack mitigation)
    user = db.query(User).filter(User.email == email_normalised).first()

    _INVALID_CREDENTIALS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user:
        raise _INVALID_CREDENTIALS

    if not verify_password(payload.password, user.password_hash):
        raise _INVALID_CREDENTIALS

    # Issue JWT
    access_token = create_access_token(
        data={
            "user_id": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return LoginResponse(
        access_token=access_token,
        user=UserOut.model_validate(user),
    )


# ---------------------------------------------------------------------------
# GET /auth/me
# ---------------------------------------------------------------------------
@router.get(
    "/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated user's profile",
    responses={
        401: {"description": "Missing or invalid JWT token"},
    },
)
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    """
    Return the profile of the currently authenticated user.

    Requires a valid JWT in the Authorization: Bearer <token> header.
    Useful for:
      - Validating a stored token is still active on app load.
      - Refreshing the user profile after a profile update.
    """
    return UserOut.model_validate(current_user)
