from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.concurrency import run_in_threadpool

from app.api.routes import router
from app.services.tagger import tagger_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_in_threadpool(tagger_service.startup)
    yield

app = FastAPI(title = "Moderation service", version = "0.1.0", lifespan=lifespan)

app.include_router(router)