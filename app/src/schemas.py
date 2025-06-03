import re
from datetime import datetime
from typing import Annotated, Generic, List, TypeVar

from pydantic import AfterValidator, BaseModel, Field


def is_url(value: str) -> str:
    http_and_https_pattern = re.compile(
        r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
    )
    if not http_and_https_pattern.match(value):
        raise ValueError("URL адрес не является корректным!")
    return value


def is_my_url(value: str) -> str:
    domen = "http://localhost:8080/"
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
    id: int
    link: str
    original_link: str
    is_active: bool
    due_date: datetime

    class Config:
        from_attributes = True


class StatisticLinkInfo(BaseModel):
    link: str
    orig_link: str
    last_hour_clicks: int = 0
    last_day_clicks: int = 0
    is_active: bool
    due_date: datetime


class PaginationInfo(BaseModel):
    page: int
    size: int
    total_pages: int
    next: bool
    prev: bool


T = TypeVar("T")


class Message(BaseModel, Generic[T]):
    links: List[T]
    info: PaginationInfo
