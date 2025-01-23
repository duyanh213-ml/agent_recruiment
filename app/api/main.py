from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.endpoints.job_endpoints import job_router
from app.api.endpoints.user_endpoint import user_router
from app.core.config import settings
from app.utils.defaults import create_admin_account, display_startup_message

from app.db.session import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    display_startup_message()
    create_admin_account()
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.include_router(job_router, prefix="/job", tags=["job"])
app.include_router(user_router, prefix="/user", tags=["user"])


@app.get("/health")
async def check_health():
    return {"status": "healthy"}
