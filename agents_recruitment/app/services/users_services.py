import datetime

from typing import Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.db.models import User
from app.schemas.user_schemas import (
    Token, UserCreate, ChangePasswordRequest, UserResponse
)
from app.core.security import (
    get_hash_password, verify_password, create_access_token
)


def register_user(user: UserCreate, db: Session):
    try:
        checked_user = db.query(User).filter(
            User.username == user.username).first()
        if checked_user:
            return JSONResponse(
                status_code=400, content="Username already registered"
            )
        new_user = User(
            name=user.name,
            username=user.username,
            hash_password=get_hash_password(user.password),
            role=settings.default_HR_role,
            is_active=settings.default_hr_active,
            created_date=datetime.datetime.now(datetime.timezone.utc),
            updated_date=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(new_user)
        db.flush()
        db.commit()
        return new_user

    except Exception as e:
        raise Exception("Error occurred in register user", e)


def login(db: Session, form_data: OAuth2PasswordRequestForm = Depends(), token_type: str = "bearer"):
    try:
        user = db.query(User).filter(
            User.username == form_data.username).first()
        if not user:
            return JSONResponse(
                status_code=401, content="Incorrect username or password")
        if not verify_password(form_data.password, user.hash_password):
            return JSONResponse(
                status_code=401, content="Incorrect username or password")
        return Token(
            access_token=create_access_token({"sub": form_data.username}),
            token_type=token_type,
            role=user.role
        )
        
    except Exception as e:
        raise Exception("Error occurred in login", e)


def get_user_role(user: Dict, db: Session):
    try:
        role = db.query(User.role).filter(
            User.username == user.get("username", "")).first()
        return role
    except Exception as e:
        raise Exception("Error occured in get user role", e)


def activate_user(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return JSONResponse(status_code=400, content="User not found")
        if user.role != settings.default_HR_role:
            return JSONResponse(status_code=400, content="This user is not HR")
        user.is_active = True
        db.flush()
        db.commit()
        return user

    except Exception as e:
        db.rollback()
        raise Exception("Error occured in activate user", e)


def change_password(username: str, change_password_request: ChangePasswordRequest, db: Session):
    try:
        user = db.query(User).filter(
            User.username == username).first()
        if not user:
            return JSONResponse(
                status_code=400, content="User does not exist")
        if not verify_password(change_password_request.old_password, user.hash_password):
            return JSONResponse(
                status_code=401, content="Incorrect password")
        user.hash_password = get_hash_password(
            change_password_request.new_password)
        user.updated_date = datetime.datetime.now(datetime.timezone.utc)
        db.flush()
        db.commit()
        return user
    except Exception as e:
        raise Exception("Error occured in change password", e)


def delete_user_by_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return JSONResponse(status_code=404, content="User not found")
        if user.role == settings.default_admin_role:
            return JSONResponse(
                status_code=400, content="Cannot delete admin")
        user_response = UserResponse(
            id=user.id,
            name=user.name,
            username=user.username,
            hash_password=user.hash_password,
            role=user.role,
            is_active=user.is_active,
            created_date=user.created_date,
            updated_date=user.updated_date,
        )
        db.delete(user)
        db.commit()
        return user_response
    except Exception as e:
        raise Exception("Error occured in delete user by id", e)
