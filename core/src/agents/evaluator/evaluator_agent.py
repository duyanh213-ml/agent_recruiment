import json
import logging
import datetime

from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.settings.settings import GeneralCoreSettings, OpenAISettings
from src.db.models import Candidate, Job
from src.agents.evaluator.schemas import JobInfo, CandidateInfo
from src.agents.evaluator.prompts import EvaluatorPrompt
from src.utils.openai_client import recruitment_openai

logger = logging.getLogger(__name__)

def get_job_info(job_id: int, db: Session):
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return JSONResponse(status_code=404, content="Job not found")

        return JobInfo(
            title=job.title,
            job_type=job.job_type,
            qualifications=job.qualifications,
            responsibilities=job.responsibilities,
            benefits=job.benefits,
            work_schedule=job.work_schedule,
            location=job.location,
        )
    except Exception as e:
        raise Exception("Error occured in get job info", e)



def get_candidate_info(candidate_id: int, db: Session):
    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return JSONResponse(status_code=404, content="Candidate not found")

        return CandidateInfo(
            extract_objective=candidate.extract_objective,
            extract_experiences=candidate.extract_experiences,
            extract_skills=candidate.extract_skills,
            extract_education=candidate.extract_education,
            extract_certificate=candidate.extract_certificate,
        )
    except Exception as e:
        raise Exception("Error occured in get candidate info", e)


def save_eval_2_db(candidate_id: int, score: int, summary_reason: str, db: Session):
    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return JSONResponse(status_code=404, content="Candidate not found")

        candidate.score = score
        candidate.summary_reason = summary_reason
        candidate.updated_date = datetime.datetime.now(datetime.timezone.utc)

        db.flush()
        db.commit()

        return candidate
    except Exception as e:
        raise Exception("Error occured in save evaluation to DB", e)


def evaluate_candidates(candidate_ids: List[int], job_id: int, db: Session):
    for candidate_id in candidate_ids:
        candidate_info = get_candidate_info(candidate_id, db)
        job_info = get_job_info(job_id, db)
        
        evaluate_candidate_prompt = EvaluatorPrompt.evaluate_candidate_prompt(
            candidate_info=candidate_info,
            job_info=job_info
        )
        
        evaluation_result = recruitment_openai.get_completions(
            prompts=evaluate_candidate_prompt,
            system_role=OpenAISettings.SYSTEM_ROLE,
            system_content=OpenAISettings.SYSTEM_CONTENT_FOR_EVALUATION
        )
        
        json_eval_data = json.loads(evaluation_result)
    
        save_eval_2_db(
            candidate_id=candidate_id,
            score=json_eval_data[GeneralCoreSettings.SCORE],
            summary_reason=json_eval_data[GeneralCoreSettings.SUMMARY_REASON],
            db=db
        )
        
        logger.info(json_eval_data)

        return json_eval_data

        