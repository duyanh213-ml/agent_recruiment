import datetime
import os
import logging
import json

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.utils.minio import minio_agent_recruiment
from src.settings.settings import GeneralCoreSettings, OpenAISettings
from src.utils.pdf_extractor import PDFExtractor
from src.agents.extractor.prompts import ExtractorPrompt
from src.utils.openai_client import recruitment_openai
from src.db.models import Candidate


logger = logging.getLogger(__name__)


def remove_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"Deleted: {file_path}")
    else:
        logger.info("File not found!")


def check_folder(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
        
def save_extract_2_db(candidate_id: int, extract_obj: str | None, extract_exp: str | None, 
            extract_skills: str | None, extract_edu: str | None, extract_cert: str | None, db: Session):
    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return JSONResponse(status_code=404, content="Candidate not found")

        candidate.extract_objective = extract_obj
        candidate.extract_experiences = extract_exp
        candidate.extract_skills = extract_skills
        candidate.extract_education = extract_edu
        candidate.extract_certificate = extract_cert
        candidate.updated_date = datetime.datetime.now(datetime.timezone.utc)

        db.flush()
        db.commit()

        return candidate
    except Exception as e:
        raise Exception("Error occured in save extracted information to DB", e)
    

def extract_candidate_cv(candidate_id: int, db: Session):
    folder_prefix = f"{candidate_id}/"
    download_path = f"{GeneralCoreSettings.TMP_CANDIDATE_FOLDER}/{candidate_id}.pdf"

    check_folder(GeneralCoreSettings.TMP_CANDIDATE_FOLDER)
    minio_agent_recruiment.download_file(
        folder_prefix, download_path
    )
    pdf_extractor = PDFExtractor()
    paragraph, is_two_step = pdf_extractor.extract_from_path(download_path)

    if is_two_step:
        correct_paragraph = recruitment_openai.get_completions(
            prompts=ExtractorPrompt.paragraph_correction_prompt(paragraph),
            system_role=OpenAISettings.SYSTEM_ROLE,
            system_content=OpenAISettings.SYSTEM_CONTENT_FOR_PARAGRAPH_CORRECTION_PROMPT
        )
        extracted_data = recruitment_openai.get_completions(
            prompts=ExtractorPrompt.extraction_prompt(correct_paragraph),
            system_role=OpenAISettings.SYSTEM_ROLE,
            system_content=OpenAISettings.SYSTEM_CONTENT_FOR_EXTRACTION
        )
    else:
        extracted_data = recruitment_openai.get_completions(
            prompts=ExtractorPrompt.extraction_prompt(paragraph),
            system_role=OpenAISettings.SYSTEM_ROLE,
            system_content=OpenAISettings.SYSTEM_CONTENT_FOR_EXTRACTION
        )
        
    json_extracted_data = json.loads(extracted_data)
    
    save_extract_2_db(
        candidate_id=candidate_id,
        extract_obj=json_extracted_data[GeneralCoreSettings.EXTRACT_OBJECTIVE],
        extract_exp=json_extracted_data[GeneralCoreSettings.EXTRACT_EXPERIENCES],
        extract_skills=json_extracted_data[GeneralCoreSettings.EXTRACT_SKILLS],
        extract_edu=json_extracted_data[GeneralCoreSettings.EXTRACT_EDUCATION],
        extract_cert=json_extracted_data[GeneralCoreSettings.EXTRACT_CERTIFICATE],
        db=db
    )
    
    remove_file(download_path)
    logger.info(json_extracted_data)

    return json_extracted_data
