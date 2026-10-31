
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_session import UserSession


def get_user_by_employee_id(db: Session, employee_id: str):
    statement = select(User).where(
        User.employee_id == employee_id
    )
    return db.scalar(statement)


def create_user_session(
    db: Session,
    user_id: int,
    token_id: str,
    expires_at: datetime,
):
    session = UserSession(
        user_id=user_id,
        token_id=token_id,
        expires_at=expires_at,
    )

    db.add(session)
    db.flush()
    return session


def get_active_session(db: Session, token_id: str):
    statement = select(UserSession).where(
        UserSession.token_id == token_id,
        UserSession.revoked_at.is_(None),
        UserSession.expires_at > datetime.now(timezone.utc),
    )
    return db.scalar(statement)


def revoke_session(db: Session, session: UserSession):
    session.revoked_at = datetime.now(timezone.utc)
    db.flush()
    return session
