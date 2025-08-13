from sqlalchemy import func, Column, Integer, Text, DateTime, Boolean, ForeignKey, Float
from src.db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, index=True, nullable=False)
    job_type = Column(Text, index=True, nullable=False)
    qualifications = Column(Text, nullable=False)
    responsibilities = Column(Text, nullable=False)
    benefits = Column(Text, nullable=False)
    work_schedule = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    is_open = Column(Boolean, nullable=False)
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True, nullable=False)
    phone_number = Column(Text, nullable=False)
    email = Column(Text, index=True, nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    job_id = Column(Integer, ForeignKey(
        "jobs.id", ondelete="SET NULL"))
    job_type = Column(Text, nullable=False)
    CV_directory = Column(Text)
    extract_objective = Column(Text)
    extract_experiences = Column(Text)
    extract_skills = Column(Text)
    extract_education = Column(Text)
    extract_certificate = Column(Text)
    score = Column(Float)
    summary_reason = Column(Text)
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())