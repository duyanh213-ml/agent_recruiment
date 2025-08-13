import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Dict, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.models import Permission, User

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 10
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict,
                        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        return {"username": username}
    except JWTError:
        raise credentials_exception


def get_user_role(username: Dict, db: Session):
    try:
        result = db.query(User.role).filter(
            User.username == username.get("username", "")).first().role
        if not result:
            raise HTTPException(
                status_code=400, detail="Username does not exist")
        return result
    except Exception as e:
        raise Exception("Error occured in get user role")


def have_permission(job_id: int, username: Dict, db: Session):
    try:
        user_id = db.query(User.id).filter(
            User.username == username.get("username", "")).first().id
        if not user_id:
            return False
        result = db.query(Permission.id).filter(Permission.user_id == user_id,
                                                Permission.job_id == job_id).first()
        return True if result else False
    except Exception as e:
        raise Exception("Error occured in check job permission")


def is_user_active(username: Dict, db: Session):
    try:
        is_active = db.query(User.is_active).filter(
            User.username == username.get("username", "")).first().is_active
        return bool(is_active)
    except Exception as e:
        raise Exception("Error occured in is user active")
