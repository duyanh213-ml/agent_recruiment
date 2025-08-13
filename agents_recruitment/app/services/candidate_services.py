import datetime
from typing import List

from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.db.models import Candidate, Job
from app.utils.defaults import format_candidate_name
from app.core.config import settings
from app.utils.minio import minio_agent_recruiment
from app.schemas.candidate_schemas import CandidateResponse, CandidateUpdate


async def apply_job(name: str, email: str, phone_number: str, year_of_birth: int, job_id: int,
                    file_upload: UploadFile, db: Session):
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return JSONResponse(status_code=400, content="Job not found")
        if not job.is_open:
            return JSONResponse(status_code=400, content="Cannot apply this job")

        new_candidate = Candidate(
            name=name,
            email=email,
            year_of_birth=year_of_birth,
            phone_number=phone_number,
            job_id=job_id,
            job_type=job.job_type,
            created_date=datetime.datetime.now(datetime.timezone.utc),
            updated_date=datetime.datetime.now(datetime.timezone.utc),
        )
        db.add(new_candidate)
        db.flush()

        current_id = new_candidate.id
        candidate_name = format_candidate_name(name)
        object_name = f"{current_id}/{candidate_name}.pdf"

        with open(settings.TMP_CANDIDATE_FILE, "wb") as buffer:
            content = await file_upload.read()
            buffer.write(content)

        minio_agent_recruiment.upload_file(
            settings.TMP_CANDIDATE_FILE, object_name)
        new_candidate.CV_directory = object_name

        db.commit()

        return new_candidate
    except Exception as e:
        raise Exception("Error occured in apply job", e)


def get_non_eval_candidates(job_id: int, db: Session):
    try:
        non_eval_candidates = db.query(Candidate).filter(
            Candidate.job_id == job_id,
            Candidate.score.is_(None)
        ).all()

        if not non_eval_candidates:
            return JSONResponse(status_code=404, content="No non-eval candidate found")

        return non_eval_candidates
    except Exception as e:
        raise Exception("Error occured in display non evaluated candidates", e)


def get_null_candidates(db: Session):
    try:
        null_candidates = db.query(Candidate).filter(
            Candidate.job_id.is_(None)
        ).all()

        if not null_candidates:
            return JSONResponse(status_code=404, content="No null candidate found")

        return null_candidates
    except Exception as e:
        raise Exception("Error occured in display null candidates", e)


def delete_candidates_from_job(candidate_ids: List[int], job_id: int, db: Session):
    try:
        candidates = db.query(Candidate).filter(
            Candidate.id.in_(candidate_ids),
            Candidate.job_id == job_id
        ).all()

        if not candidates:
            return JSONResponse(status_code=404, content="No candidate found")

        for candidate in candidates:
            candidate.job_id = None
            candidate.updated_date = datetime.datetime.now(
                datetime.timezone.utc)

        db.flush()
        db.commit()

    except Exception as e:
        raise Exception("Error occured in delete candidates from job", e)


def assign_candidate_to_job(candidate_id: int, job_id: int, db: Session):
    try:
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id).first()

        if not candidate:
            return JSONResponse(status_code=404, content="Candidate not found")

        candidate.job_id = job_id
        candidate.updated_date = datetime.datetime.now(
            datetime.timezone.utc)

        db.flush()
        db.commit()
    except Exception as e:
        raise Exception("Error occured in assign candidate to job", e)


def update_candidate(candidate_update: CandidateUpdate, db: Session):
    try:
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_update.id,
            Candidate.job_id == candidate_update.job_id
        ).first()
        if not candidate:
            return JSONResponse(status_code=404, content="Candidate not found")

        is_updated = False

        if candidate_update.name is not None:
            is_updated = True
            candidate.name = candidate_update.name
        if candidate_update.email is not None:
            is_updated = True
            candidate.email = candidate_update.email
        if candidate_update.phone_number is not None:
            is_updated = True
            candidate.phone_number = candidate_update.phone_number
        if candidate_update.year_of_birth is not None:
            is_updated = True
            candidate.year_of_birth = candidate_update.year_of_birth

        if is_updated:
            candidate.updated_date = datetime.datetime.now(
                datetime.timezone.utc)

        db.flush()
        db.commit()

        return candidate
    except Exception as e:
        raise Exception("Error occured in update candidate", e)


def delete_candidates_from_system(candidate_ids: List[int], db: Session):
    try:
        candidates = db.query(Candidate).filter(
            Candidate.id.in_(candidate_ids)).all()

        if not candidates:
            return JSONResponse(status_code=404, content="No candidate found")

        candidate_responses = [
            CandidateResponse(
                id=candidate.id,
                name=candidate.name,
                email=candidate.email,
                phone_number=candidate.phone_number,
                year_of_birth=candidate.year_of_birth,
                job_id=candidate.job_id,
                job_type=candidate.job_type,
                CV_directory=candidate.CV_directory,
                extract_objective=candidate.extract_objective,
                extract_experiences=candidate.extract_experiences,
                extract_skills=candidate.extract_skills,
                extract_education=candidate.extract_education,
                extract_certificate=candidate.extract_certificate,
                score=candidate.score,
                summary_reason=candidate.summary_reason,
                created_date=candidate.created_date,
                updated_date=candidate.updated_date
            )
            for candidate in candidates
        ]

        db.execute(delete(Candidate).where(Candidate.id.in_(candidate_ids)))
        db.commit()

        return candidate_responses
    except Exception as e:
        raise Exception("Error occured in delete candidate from system", e)
