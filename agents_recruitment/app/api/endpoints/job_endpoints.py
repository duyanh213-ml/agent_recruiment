from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, List

from app.schemas.job_schemas import (
    JobCreate, JobResponse, PaginationBase,
    JobUpdate, PermissionResponse, FilterJobRequest
)
from app.services.jobs_services import (
    assign_permission, create_job, get_all_job, get_job_by_id,
    update_job_by_id, delete_job_by_id, get_all_job_not_in_permission
)
from app.db.session import get_db
from app.core.config import settings
from app.core.security import (
    have_permission, get_current_user,
    get_user_role, is_user_active
)

job_router = APIRouter()


@job_router.post("/create_job", response_model=JobResponse, status_code=201)
async def create_job_api(new_job: JobCreate, db: Session = Depends(get_db),
                         current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return create_job(new_job, db, current_user)


@job_router.post("/get_jobs", response_model=List[JobResponse], status_code=201)
async def get_all_jobs_api(filter_job: FilterJobRequest, pagination_base: PaginationBase,
                           db: Session = Depends(get_db),
                           current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return get_all_job(filter_job, pagination_base, db)


@job_router.post("/get_empty_jobs", response_model=List[JobResponse], status_code=201)
async def get_all_jobs_not_in_permission_api(filter_job: FilterJobRequest, pagination_base: PaginationBase,
                                             db: Session = Depends(get_db),
                                             current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_admin_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return get_all_job_not_in_permission(filter_job, pagination_base, db)


@job_router.post("/get_job", response_model=JobResponse, status_code=201)
async def get_job_by_id_api(job_id: int, db: Session = Depends(get_db),
                            current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return get_job_by_id(job_id, db)


@job_router.post("/assign_permission", response_model=PermissionResponse, status_code=201)
async def assign_permission_api(job_id: int, user_id: int, db: Session = Depends(get_db),
                                current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    # Check if user is HR, not admin
    if user_role not in [settings.default_admin_role]:
        if not have_permission(job_id, current_user, db):   # Check if HR has permission
            return JSONResponse(status_code=403, content="Not authorized")
    return assign_permission(user_id, job_id, db)


@job_router.post("/update_job", response_model=JobResponse, status_code=201)
async def update_job_by_id_api(job_update: JobUpdate, db: Session = Depends(get_db),
                               current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role] or not have_permission(job_update.id, current_user, db):
        return JSONResponse(status_code=403, content="Not authorized")
    return update_job_by_id(job_update, db)


@job_router.post("/delete_job", response_model=JobResponse, status_code=201)
async def delete_job_by_id_api(job_id: int, db: Session = Depends(get_db),
                               current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role] or not have_permission(job_id, current_user, db):
        return JSONResponse(status_code=403, content="Not authorized")
    return delete_job_by_id(job_id, db)
