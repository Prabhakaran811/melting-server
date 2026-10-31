
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User


def ensure_initial_admin(db: Session) -> None:
    existing_admin = db.scalar(
        select(User).where(
            User.employee_id == settings.ADMIN_EMPLOYEE_ID
        )
    )

    if existing_admin:
        print("Initial Admin already exists. Skipping creation.")
        return

    admin = User(
        employee_id=settings.ADMIN_EMPLOYEE_ID,
        full_name=settings.ADMIN_FULL_NAME,
        email=settings.ADMIN_EMAIL.lower(),
        phone_number=settings.ADMIN_PHONE,
        password_hash=hash_password(settings.ADMIN_PASSWORD),
        role="admin",
        is_active=True,
    )

    db.add(admin)

    try:
        db.commit()
        print("Initial Admin created successfully.")
    except Exception:
        db.rollback()
        raise
