from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, Query
from typing import Dict, Optional

from app.db.models import (
    Job, Permission, User
)
from app.schemas.job_schemas import (
    JobCreate, JobResponse, PaginationBase,
    JobUpdate, FilterJobRequest
)
from app.core.config import settings


def create_job(job_create: JobCreate, db: Session, current_user: Dict):
    try:
        new_job = Job(
            title=job_create.title,
            job_type=job_create.job_type,
            qualifications=job_create.qualifications,
            responsibilities=job_create.responsibilities,
            benefits=job_create.benefits,
            work_schedule=job_create.work_schedule,
            location=job_create.location,
            created_date=job_create.created_date,
            updated_date=job_create.updated_date
        )
        db.add(new_job)
        db.flush()  # Ensures `new_job.id` is available before the next query

        # Establish a permission for the user who created the job
        user_id = db.query(User.id).filter(
            User.username == current_user.get("username", "")
        ).scalar()
        if not user_id:
            return JSONResponse(status_code=400, content="User not found")

        new_permission = Permission(
            job_id=new_job.id,
            user_id=user_id,
            created_date=job_create.created_date,
            updated_date=job_create.updated_date
        )
        db.add(new_permission)
        db.commit()

        return new_job
    except Exception as e:
        raise Exception("Error occurred in create job:", e)


def apply_job_filters(query: Query, filter_job: FilterJobRequest):
    if filter_job.title is not None:
        # Use ilike for case-insensitive search
        query = query.filter(Job.title.ilike(f"%{filter_job.title}%"))
    if filter_job.job_type is not None:
        query = query.filter(Job.job_type.ilike(
            f"%{filter_job.job_type}%"))
    if filter_job.location is not None:
        query = query.filter(Job.location.ilike(
            f"%{filter_job.location}%"))
    return query


def get_all_job(filter_job: FilterJobRequest, pagination_base: PaginationBase, db: Session):
    try:
        query = db.query(Job)
        query = apply_job_filters(query, filter_job)
        result = query.order_by(desc(Job.updated_date)) \
            .limit(pagination_base.limit) \
            .offset(pagination_base.offset).all()
        return result

    except Exception as e:
        raise Exception("Error occured in get all job:", e)


def get_all_job_not_in_permission(filter_job: FilterJobRequest, pagination_base: PaginationBase, db: Session):
    try:
        sub_query = select(Permission.job_id).subquery()
        query = db.query(Job).filter(Job.id.not_in(sub_query))
        query = apply_job_filters(query, filter_job)
        result = query.order_by(desc(Job.updated_date)) \
            .limit(pagination_base.limit) \
            .offset(pagination_base.offset).all()
        return result

    except Exception as e:
        raise Exception("Error occured in get all job not in permission", e)


def get_job_by_id(job_id: int, db: Session):
    try:
        job = db.query(Job) \
            .where(Job.id == job_id).first()
        if not job:
            return JSONResponse(status_code=400, content="Job not found")
        return job
    except Exception as e:
        raise Exception("Error occured in get job by id:", e)


def assign_permission(user_id: int, job_id: int, db: Session):
    try:
        user = db.query(User.id, User.role).filter(User.id == user_id).first()
        job_id_check = db.query(Job.id).filter(Job.id == job_id).first()
                
        if not user or not job_id_check:
            return JSONResponse(status_code=400, content="User or job not found")
        if user.role == settings.default_admin_role:
            return JSONResponse(status_code=400, content="Cannot assign job for admin")
        
        new_permission = Permission(
            job_id=job_id,
            user_id=user_id,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
     
        db.add(new_permission)
        db.flush()
        db.commit()
        return new_permission
    except Exception as e:
        raise Exception("Error occured in assign permission", e)


def update_job_by_id(job_update: JobUpdate, db: Session):
    try:
        job = db.query(Job).filter(Job.id == job_update.id).first()
        if not job:
            return JSONResponse(status_code=404, content="Job not found")

        is_updated = False

        if job_update.title is not None:
            is_updated = True
            job.title = job_update.title
        if job_update.job_type is not None:
            is_updated = True
            job.job_type = job_update.job_type
        if job_update.qualifications is not None:
            is_updated = True
            job.qualifications = job_update.qualifications
        if job_update.responsibilities is not None:
            is_updated = True
            job.responsibilities = job_update.responsibilities
        if job_update.benefits is not None:
            is_updated = True
            job.benefits = job_update.benefits
        if job_update.work_schedule is not None:
            is_updated = True
            job.work_schedule = job_update.work_schedule
        if job_update.location is not None:
            is_updated = True
            job.location = job_update.location

        if is_updated:
            job.updated_date = func.now()

        db.flush()
        db.commit()

        return job
    except Exception as e:
        raise Exception("Error occured in update job by id:", e)


def delete_job_by_id(job_id: int, db: Session):
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return JSONResponse(status_code=404, content="Job not found")
        job_response = JobResponse(
            id=job.id,
            title=job.title,
            job_type=job.job_type,
            qualifications=job.qualifications,
            responsibilities=job.responsibilities,
            benefits=job.benefits,
            work_schedule=job.work_schedule,
            location=job.location,
            created_date=job.created_date,
            updated_date=job.updated_date
        )
        db.delete(job)
        db.commit()
        return job_response
    except Exception as e:
        raise Exception("Error occured in delete job by id:", e)
