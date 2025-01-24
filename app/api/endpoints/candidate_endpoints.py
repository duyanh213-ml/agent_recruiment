from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.candidate_schemas import CandidateResponse, ApplyJobRequest
from app.services.candidate_services import (
    apply_job
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

