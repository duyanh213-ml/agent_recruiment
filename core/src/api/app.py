from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Depends, HTTPException, status, Body, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing import List

from src.settings.settings import GeneralCoreSettings, display_startup_message
from src.agents.extractor.extractor_agent import extract_candidate_cv
from src.agents.evaluator.evaluator_agent import evaluate_candidates
from src.db.session import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    display_startup_message()
    yield

app = FastAPI(lifespan=lifespan, title=GeneralCoreSettings.APP_TITLE)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Dùng HTTPBearer thay vì OAuth2PasswordBearer
security_scheme = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    if token != GeneralCoreSettings.TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


router = APIRouter(prefix=GeneralCoreSettings.PREFIX)


@router.get("/health/")
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.post("/extract_candidate_cv/")
def extract_candidate_cv_api(
    background_tasks: BackgroundTasks,
    candidate_id: int = Body(..., embed=True),
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    background_tasks.add_task(extract_candidate_cv, candidate_id, db)
    return {"message": f"Candidate id {candidate_id} is extracted"}


@router.post("/evaluate_candidate")
def evaluate(
    background_tasks: BackgroundTasks,
    candidate_ids: List[int] = Body(..., embed=True),
    job_id: int = Body(..., embed=True),
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    background_tasks.add_task(evaluate_candidates, candidate_ids, job_id, db)
    return {"message": f"Candidate \"{candidate_ids}\" are evaluated"}


app.include_router(router)
