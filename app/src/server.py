from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.src.router import router
from app.src.db import init_db_tortoise


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:

    await init_db_tortoise(_app)
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
