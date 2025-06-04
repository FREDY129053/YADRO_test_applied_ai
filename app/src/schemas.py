import os
import re
from datetime import datetime
from typing import Annotated, Generic, List, TypeVar

from pydantic import AfterValidator, BaseModel, Field


def is_url(value: str) -> str:
    """Валидация URL адресов

    Args:
        value (str): значение для валидации

    Raises:
        ValueError: неверный URL адрес

    Returns:
        str: URL адрес
    """
    value = value.strip()
    http_and_https_pattern = re.compile(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+")
    if not http_and_https_pattern.match(value):
        raise ValueError("URL адрес не является корректным!")
    return value


def is_my_url(value: str) -> str:
    """Проверка, что передаваемый URL "мой" адрес(с localhost:8080)

    Args:
        value (str): URL адрес

    Raises:
        ValueError: URL адрес сгенерирован не этим сервисом

    Returns:
        str: URL адрес
    """
    value = value.strip()
    domen = f"{os.getenv('DOMEN')}/"
    my_url = re.compile(r"^%s.{9}$" % domen)
    if not my_url.match(value):
        raise ValueError("URL адрес сгенерирован не этим сервисом")
    return value


class CreateShortLink(BaseModel):
    url: Annotated[
        str, Field(description="Сссылка, которую надо укоротить"), AfterValidator(is_url)
    ]


class DeactivateShortLink(BaseModel):
    short_url: Annotated[
        str, Field(description="Сссылка, которую надо деактивировать"), AfterValidator(is_my_url)
    ]


class LinkInfo(BaseModel):
    id: int = Field(description="ID ссылки в сервисе")
    link: str = Field(description="Сгенерированная(короткая) ссылка")
    original_link: str = Field(description="Оригинальная(длинная) ссылка")
    is_active: bool = Field(description="Является ли ссылка активной")
    due_date: datetime = Field(description="Дата и время истечения активности ссылки")

    class Config:
        from_attributes = True


class StatisticLinkInfo(BaseModel):
    link: str = Field(description="Короткая(сгенерированная) ссылка")
    orig_link: str = Field(description="Оригинальная(длинная) ссылка")
    last_hour_clicks: int = Field(default=0, description="Кол-во посещений ссылки за последний час")
    last_day_clicks: int = Field(default=0, description="Кол-во посещений ссылки за последний день")
    is_active: bool = Field(description="Является ли ссылка активной")
    due_date: datetime = Field(description="Дата и время истечения активности ссылки")


class PaginationInfo(BaseModel):
    page: int = Field(description="Текущая страницы")
    size: int = Field(description="Размер выборки страницы")
    total_pages: int = Field(description="Суммарное кол-во страниц")
    next: bool = Field(description="Имеется ли следующая страница")
    prev: bool = Field(description="Имеется ли предыдущая страница")


T = TypeVar("T")


class Message(BaseModel, Generic[T]):
    links: List[T] = Field(description="Список ссылок")
    info: PaginationInfo = Field(description="Информация о пагинации выборки")


class ErrorSchema(BaseModel):
    detail: str = Field(description="Описание ошибки")
