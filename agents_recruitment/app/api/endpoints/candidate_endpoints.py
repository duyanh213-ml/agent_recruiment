from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, List

from app.core.config import settings
from app.core.security import get_current_user, get_user_role, have_permission, is_user_active
from app.db.session import get_db
from app.schemas.candidate_schemas import CandidateResponse
from app.services.candidate_services import (
    apply_job, delete_candidates_from_job, delete_candidates_from_system,
    get_non_eval_candidates, get_null_candidates, assign_candidate_to_job,
    update_candidate
)

candidate_route = APIRouter()


@candidate_route.post("/apply_job", response_model=CandidateResponse, status_code=201)
async def apply_job_api(name: str,
                        email: str,
                        phone_number: str,
                        year_of_birth: int,
                        job_id: int, 
                        file_upload: UploadFile = File(...), 
                        db: Session = Depends(get_db)):
    return await apply_job(name, email, phone_number, year_of_birth, job_id, file_upload, db)


@candidate_route.post("/display_non_eval_candidates", response_model=List[CandidateResponse], status_code=201)
async def display_non_eval_candidates_api(job_id: int, db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role] or not have_permission(job_id, current_user, db):
        return JSONResponse(status_code=403, content="Not authorized")
    return get_non_eval_candidates(job_id, db)


@candidate_route.post("/display_null_candidates", response_model=List[CandidateResponse], status_code=201)
async def display_null_candidates_api(db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_admin_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return get_null_candidates(db)


@candidate_route.post("/delete_candidates_from_job", response_model=List[CandidateResponse], status_code=201)
async def delete_candidates_from_job_api(candidate_ids: List[int], job_id: int, db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role] or not have_permission(job_id, current_user, db):
        return JSONResponse(status_code=403, content="Not authorized")
    return delete_candidates_from_job(candidate_ids, job_id, db)


@candidate_route.post("/assign_candidate_to_job", response_model=CandidateResponse, status_code=201)
async def assign_candidate_to_job_api(candidate_id: int, job_id: int, db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_admin_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return assign_candidate_to_job(candidate_id, job_id, db)


@candidate_route.post("/update_candidate", response_model=CandidateResponse, status_code=201)
async def update_candidate_api(candidate_id: int, job_id: int, db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_HR_role] or not have_permission(job_id, current_user, db):
        return JSONResponse(status_code=403, content="Not authorized")
    return update_candidate(candidate_id, job_id, db)


@candidate_route.post("/delete_candidates_from_system", response_model=List[CandidateResponse], status_code=201)
async def delete_candidates_from_system_api(candidate_ids: List[int], db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
    if not is_user_active(current_user, db):
        return JSONResponse(status_code=401, content="Not active")
    user_role = get_user_role(current_user, db)
    if user_role not in [settings.default_admin_role]:
        return JSONResponse(status_code=403, content="Not authorized")
    return delete_candidates_from_system(candidate_ids, db)







