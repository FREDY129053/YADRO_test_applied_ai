import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv


def load_environment():
    """Загрузка переменных окружения в зависимости от среды"""

    env_file = f"{Path(__file__).resolve().parent}/.env"

    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        raise FileExistsError(f"Файл {env_file} не найден! Создайте его")

    return dotenv_values(env_file).keys()


def validate_environment() -> None:
    required_vars = [
        "EXPIRE_MINUTES",
        "DB_PORT",
        "DB_HOST",
        "DB_NAME",
        "DB_USERNAME",
        "DB_PASSWORD",
        "DOMEN",
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Пропущены переменные: {missing}")
    is_right_minutes = int(os.getenv("EXPIRE_MINUTES", "")) > 0
    if not is_right_minutes:
        raise EnvironmentError("Минуты должны быть больше 0")
