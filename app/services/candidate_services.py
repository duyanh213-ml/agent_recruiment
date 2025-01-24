import shutil

from fastapi import UploadFile
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.candidate_schemas import ApplyJobRequest, CandidateResponse
from app.db.models import Candidate
from app.utils.defaults import format_candidate_name
from app.core.config import settings
from app.utils.minio import minio_agent_recruiment


async def apply_job(name: str, email: str, phone_number: str, year_of_birth: int, job_id: int, 
        file_upload: UploadFile, db: Session):
    try:
        new_candidate = Candidate(
            name=name,
            email=email,
            year_of_birth=year_of_birth,
            phone_number=phone_number,
            created_date=datetime.now(),
            updated_date=datetime.now(),
        )
        db.add(new_candidate)
        db.flush()
        
        current_id = new_candidate.id
        candidate_name = format_candidate_name(name)
        object_name = f"{current_id}/{candidate_name}.pdf"
        print("@" * 200)
        
        with open(settings.TMP_CANDIDATE_FILE, "wb") as buffer:
            content = await file_upload.read()
            buffer.write(content)
        print("*" * 200)
        
        minio_agent_recruiment.upload_file(settings.TMP_CANDIDATE_FILE, object_name)
        
        new_candidate.CV_directory = object_name
        db.commit()
        
        return new_candidate
    except Exception as e:
        raise Exception("Error occured in apply job", e)