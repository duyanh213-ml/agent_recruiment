from pydantic import BaseModel


class JobInfo(BaseModel):
    title: str
    job_type: str
    qualifications: str
    responsibilities: str
    benefits: str
    work_schedule: str
    location: str


class CandidateInfo(BaseModel):
    extract_objective: str
    extract_experiences: str
    extract_skills: str
    extract_education: str
    extract_certificate: str
