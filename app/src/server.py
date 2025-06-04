from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.src.router import router
from app.src.db import init_db_tortoise
from app.src.repository import change_expired_links_status

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db_tortoise(_app)
    
    scheduler.add_job(
        change_expired_links_status,
        CronTrigger(second='*/30')
    )
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
