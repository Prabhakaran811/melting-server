
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import jwt

from app.db.database import get_db
from app.core.config import settings
from app.core.security import decode_access_token
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.services import auth_service
from app.repositories import auth_repository, user_repository


router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        token, expires_at, user = auth_service.login_user(
            db,
            request.employee_id,
            request.password,
        )

        return LoginResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error),
        )


def get_current_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
        token_id = payload["jti"]
    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    session = auth_repository.get_active_session(db, token_id)

    if not session or session.user_id != user_id:
        raise HTTPException(
            status_code=401,
            detail="Session is invalid or logged out",
        )

    user = user_repository.get_by_id(db, user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is inactive or does not exist",
        )

    return user, token_id


@router.get("/me")
def get_logged_in_user(
    auth=Depends(get_current_auth),
):
    user, token_id = auth
    return {
        "id": user.id,
        "employee_id": user.employee_id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }


@router.post("/logout")
def logout(
    auth=Depends(get_current_auth),
    db: Session = Depends(get_db),
):
    user, token_id = auth

    try:
        auth_service.logout_user(db, token_id)
        return {"message": "Logout successful"}
    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error),
        )
