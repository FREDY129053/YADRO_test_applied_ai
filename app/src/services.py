import random
import string
from datetime import datetime, timedelta, timezone

import app.src.repository as URLRepository
from app.src.schemas import LinkInfo, Message, PaginationInfo, StatisticLinkInfo

domen = "http://localhost:8080/"


async def get_all_links(filter: str, page: int, size: int) -> Message[LinkInfo]:
    offset_min, offset_max = (page - 1) * size, page * size
    match filter:
        case "active":
            link_type = True
        case "inactive":
            link_type = False
        case _:
            link_type = None
    links, total = await URLRepository.get_all_links(
        type=link_type, offset_min=offset_min, offset_max=offset_max
    )
    total_pages = max(0, (total + size - 1) // size)
    return Message(
        links=links,
        info=PaginationInfo(
            page=page,
            size=size,
            total_pages=total_pages,
            next=page < total_pages - 1,
            prev=page > 1,
        ),
    )  # type: ignore


async def get_stats(page: int, size: int) -> Message[StatisticLinkInfo]:
    offset_min, offset_max = (page - 1) * size, page * size
    links, total = await URLRepository.get_all_links(offset_min=offset_min, offset_max=offset_max)
    res = []
    for link_data in links:
        stats = await URLRepository.get_stats(link_id=link_data.id)
        temp_stat = StatisticLinkInfo(
            link=link_data.link,
            orig_link=link_data.original_link,
            last_hour_clicks=stats["hour_stats"],
            last_day_clicks=stats["day_stats"],
            is_active=link_data.is_active,
            due_date=link_data.due_date,
        )
        res.append(temp_stat)

    res.sort(key=lambda x: (-x.last_day_clicks, -x.last_hour_clicks))
    total_pages = max(0, (total + size - 1) // size)
    return Message(
        links=res,
        info=PaginationInfo(
            page=page,
            size=size,
            total_pages=total_pages,
            next=page < total_pages - 1,
            prev=page > 1,
        ),
    )


async def generate_url(url: str) -> str | None:
    short_token = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(9)
    )
    short_link = f"{domen}{short_token}"
    due_date = datetime.now(timezone.utc) + timedelta(minutes=1)
    is_in_db = await URLRepository.write_short_link(
        original_link=url, short_link=short_link, due_date=due_date
    )
    if not is_in_db:
        return None
    return short_link


async def get_original_url(short_link: str) -> str | None:
    short_link = domen + short_link
    result = await URLRepository.get_orig_link(short_link=short_link)
    if not result or not result.is_active:
        return None

    if datetime.now(timezone.utc) > result.due_date:
        await URLRepository.change_activate_status(short_link=short_link)
        return None

    await URLRepository.change_statistic(short_link=short_link)
    return result.original_link


async def deactivate_link(link: str) -> bool:
    return await URLRepository.change_activate_status(short_link=link)
