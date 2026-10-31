
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.repositories import user_repository


password_hasher = PasswordHash.recommended()


def create_user(db: Session, user_data: UserCreate) -> User:

    email = str(user_data.email).strip().lower()

    # Check duplicate employee ID
    existing_employee = user_repository.get_by_employee_id(
        db, user_data.employee_id
    )

    if existing_employee:
        raise ValueError("Employee ID already exists")

    # Check duplicate email
    existing_email = user_repository.get_by_email(db, email)

    if existing_email:
        raise ValueError("Email already exists")

    # Hash password
    password_hash = password_hasher.hash(user_data.password)

    new_user_data = user_data.model_dump(
        exclude={"password"}
    )

    new_user_data["email"] = email
    new_user_data["password_hash"] = password_hash
    new_user_data["role"] = user_data.role.value

    try:
        user = user_repository.create(db, new_user_data)
        db.commit()
        return user

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Employee ID or email already exists"
        )


def get_user(db: Session, user_id: int):
    return user_repository.get_by_id(db, user_id)


def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 50,
):
    return user_repository.get_all(db, skip, limit)


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
):
    user = user_repository.get_by_id(db, user_id)

    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] is not None:
        email = str(update_data["email"]).strip().lower()

        existing_email = user_repository.get_by_email(db, email)

        if existing_email and existing_email.id != user_id:
            raise ValueError("Email already exists")

        update_data["email"] = email

    if "role" in update_data and update_data["role"] is not None:
        update_data["role"] = update_data["role"].value

    try:
        updated_user = user_repository.update(
            db, user, update_data
        )

        db.commit()
        return updated_user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")


def deactivate_user(db: Session, user_id: int):
    user = user_repository.get_by_id(db, user_id)

    if not user:
        return None

    if not user.is_active:
        return user

    try:
        user = user_repository.deactivate(db, user)
        db.commit()
        return user

    except IntegrityError:
        db.rollback()
        raise




def activate_user(db: Session, user_id: int):
    user = user_repository.get_by_id(db, user_id)

    if not user:
        return None

    if user.is_active:
        return user

    try:
        user.is_active = True
        db.commit()
        db.refresh(user)
        return user

    except Exception:
        db.rollback()
        raise


def delete_user(db: Session, user_id: int):
    user = user_repository.get_by_id(db, user_id)

    if not user:
        return None

    try:
        user_repository.delete(db, user)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise
