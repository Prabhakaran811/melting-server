
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
)
from app.repositories import auth_repository


def login_user(db: Session, employee_id: str, password: str):
    user = auth_repository.get_user_by_employee_id(
        db, employee_id
    )

    if not user:
        raise ValueError("Invalid Employee ID or password")

    if not user.is_active:
        raise ValueError("Your account is inactive")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid Employee ID or password")

    token, token_id, expires_at = create_access_token(user.id)

    try:
        auth_repository.create_user_session(
            db=db,
            user_id=user.id,
            token_id=token_id,
            expires_at=expires_at,
        )

        db.commit()
        return token, expires_at, user

    except Exception:
        db.rollback()
        raise


def logout_user(db: Session, token_id: str):
    session = auth_repository.get_active_session(db, token_id)

    if not session:
        raise ValueError("Session is already invalid or expired")

    try:
        auth_repository.revoke_session(db, session)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise
