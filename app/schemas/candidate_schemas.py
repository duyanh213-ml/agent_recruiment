from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile, File

class CandidateBase(BaseModel):
    name: str
    email: str
    phone_number: str
    year_of_birth: int
    CV_directory: Optional[str] = None
    extract_objective: Optional[str] = None
    extract_experiences: Optional[str] = None
    extract_skills: Optional[str] = None
    extract_education: Optional[str] = None
    extract_certificate: Optional[str] = None
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()


class CandidateResponse(CandidateBase):
    id: int
    
    class Config:
        orm_mode = True
        
        
class ApplyJobRequest(BaseModel):
    name: str
    email: str
    phone_number: str
    year_of_birth: int
    job_id: int