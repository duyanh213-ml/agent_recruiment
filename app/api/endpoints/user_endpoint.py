from typing import Dict
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_user_role
from app.db.session import get_db
from app.core.config import settings
from app.schemas.user_schemas import (
    UserCreate, UserResponse, Token, ChangePasswordRequest
)
from app.services.users_services import (
    delete_user_by_id, register_user, login,
    activate_user, change_password
)

user_router = APIRouter()


@user_router.post("/register_user", response_model=UserResponse, status_code=201)
def register_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@user_router.post("/token", response_model=Token, status_code=201)
def login_api(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login(db, form_data)


@user_router.post("/activate_user", response_model=UserResponse, status_code=201)
def activate_user_api(user_id: int, db: Session = Depends(get_db),
                      current_user: Dict = Depends(get_current_user)):
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_admin_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return activate_user(user_id, db)


@user_router.post("/change_password", response_model=UserResponse, status_code=201)
def change_password_api(change_password_request: ChangePasswordRequest, db: Session = Depends(get_db),
                        current_user: Dict = Depends(get_current_user)):
    return change_password(current_user.get("username", ""), change_password_request, db)


@user_router.post("/delete_user", response_model=UserResponse, status_code=201)
def delete_user_api(user_id: int, db: Session = Depends(get_db),
                    current_user: Dict = Depends(get_current_user)):
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_admin_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return delete_user_by_id(user_id, db)
