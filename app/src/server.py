from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.src.config.load_env import load_environment, validate_environment
from app.src.db import init_db_tortoise
from app.src.repository import change_expired_links_status
from app.src.router import router

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    load_environment()
    validate_environment()
    await init_db_tortoise(_app)

    scheduler.add_job(change_expired_links_status, CronTrigger(second="*/15"))
    scheduler.start()
    yield


def create_app() -> FastAPI:
    _app = FastAPI(
        title="URL Shorter API",
        docs_url="/docs",
        lifespan=lifespan,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(router=router)

    return _app


app = create_app()
