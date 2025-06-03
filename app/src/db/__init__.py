from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


async def init_db_tortoise(_app: FastAPI):

    TORTOISE_ORM = {
        "connections": {
            "default": "postgres://postgres:12345@localhost:5433/url_shorter_db"
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
