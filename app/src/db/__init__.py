import os

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


async def init_db_tortoise(_app: FastAPI):
    TORTOISE_ORM = {
        "connections": {
            "default": f"postgres://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        },
        "apps": {
            "models": {
                "models": ["app.src.db.models"],
                "default_connection": "default",
            }
        },
    }

    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    register_tortoise(
        app=_app,
        config=TORTOISE_ORM,
    )
