from sqlalchemy import func, Column, Integer, Text, DateTime, Boolean, ForeignKey
from app.db.session import Base


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
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True, nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    CV_directory = Column(Text, nullable=False)
    extract_objective = Column(Text)
    extract_experiences = Column(Text)
    extract_skills = Column(Text)
    extract_education = Column(Text)
    extract_certificate = Column(Text)
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())


class Job_Candidate(Base):
    __tablename__ = "job_candidate"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey(
        "jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    candidate_id = Column(
        Integer, ForeignKey("candidates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    score = Column(Integer, index=True)
    summary_reason = Column(Text)
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True, nullable=False)
    username = Column(Text, unique=True, index=True, nullable=False)
    hash_password = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey(
        "jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                     index=True, nullable=False)
    created_date = Column(DateTime, nullable=False, default=func.now())
    updated_date = Column(DateTime, nullable=False, default=func.now())
