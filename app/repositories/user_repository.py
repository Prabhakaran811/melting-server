
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_id(db: Session, user_id: int):
    statement = select(User).where(User.id == user_id)
    return db.scalar(statement)


def get_by_email(db: Session, email: str):
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def get_by_employee_id(db: Session, employee_id: str):
    statement = select(User).where(
        User.employee_id == employee_id
    )
    return db.scalar(statement)


def get_all(db: Session, skip: int = 0, limit: int = 50):
    statement = (
        select(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def create(db: Session, user_data: dict):
    user = User(**user_data)

    db.add(user)
    db.flush()
    db.refresh(user)

    return user


def update(db: Session, user: User, update_data: dict):
    for field, value in update_data.items():
        setattr(user, field, value)

    db.flush()
    db.refresh(user)

    return user


def deactivate(db: Session, user: User):
    user.is_active = False

    db.flush()
    db.refresh(user)

    return user



def delete(db: Session, user: User):
    db.delete(user)
    db.flush()

    return user