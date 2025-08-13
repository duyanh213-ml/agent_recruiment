from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CandidateBase(BaseModel):
    name: str
    email: str
    phone_number: str
    year_of_birth: int
    job_id: Optional[int] = None
    job_type: str
    CV_directory: Optional[str] = None
    extract_objective: Optional[str] = None
    extract_experiences: Optional[str] = None
    extract_skills: Optional[str] = None
    extract_education: Optional[str] = None
    extract_certificate: Optional[str] = None
    score: Optional[float] = None
    summary_reason: Optional[str] = None
    created_date: datetime
    updated_date: datetime


class CandidateResponse(CandidateBase):
    id: int

    class Config:
        orm_mode = True


class CandidateUpdate(BaseModel):
    id: int
    job_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    year_of_birth: Optional[int] = None
