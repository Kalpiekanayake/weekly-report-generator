"""
routers/auth.py
---------------
Authentication endpoints: register, login, and get-current-user (me).

Design decisions:
  - Register immediately returns a JWT so the user is logged in after sign-up.
  - Login returns both the token AND the user profile in one response
    (LoginResponse) so the frontend doesn't need a follow-up /me call.
  - /me is kept for token refresh validation / profile re-fetch scenarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserOut, LoginResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------
@router.post(
    "/register",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.

    - Validates that the email is not already taken.
    - Hashes the password with bcrypt before storing.
    - Returns a JWT + user profile so the client is immediately authenticated.
    """
    # 1. Check for duplicate email (case-insensitive)
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists.",
        )

    # 2. Hash password — never store plain text
    hashed_pw = get_password_hash(payload.password)

    # 3. Persist new user
    new_user = User(
        email=payload.email.lower(),
        password_hash=hashed_pw,
        full_name=payload.full_name.strip(),
        role=payload.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4. Issue JWT
    token = create_access_token(
        data={
            "user_id": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role,
        }
    )

    return LoginResponse(
        access_token=token,
        user=UserOut.model_validate(new_user),
    )


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------
@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate and receive a JWT",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate an existing user.

    - Looks up user by email.
    - Verifies bcrypt password hash.
    - Returns a JWT + user profile.

    WHY a generic error message: returning "wrong password" vs "email not found"
    separately would leak information about which emails are registered
    (user enumeration attack). One generic message prevents this.
    """
    user = db.query(User).filter(User.email == payload.email.lower()).first()

    # Generic message on both "not found" and "wrong password"
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        data={
            "user_id": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    return LoginResponse(
        access_token=token,
        user=UserOut.model_validate(user),
    )


# ---------------------------------------------------------------------------
# GET /auth/me
# ---------------------------------------------------------------------------
@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current authenticated user's profile",
)
def me(current_user: User = Depends(get_current_user)):
    """
    Returns the profile of the currently authenticated user.
    Useful for token validation and profile refresh on page load.
    """
    return UserOut.model_validate(current_user)
