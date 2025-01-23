from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class JobBase(BaseModel):
    title: str
    job_type: str
    qualifications: str
    responsibilities: str
    benefits: str
    work_schedule: str
    location: str
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int

    class Config:
        orm_mode = True


class PaginationBase(BaseModel):
    limit: int
    offset: int


class SearchJob(PaginationBase):
    title: Optional[str] = None
    job_type: Optional[str] = None


class JobUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    job_type: Optional[str] = None
    qualifications: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    work_schedule: Optional[str] = None
    location: Optional[str] = None


class PermissionResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    created_date: datetime
    updated_date: datetime


class FilterJobRequest(BaseModel):
    title: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
