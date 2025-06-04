from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

from app.src.db.models import URLInfo, URLRedirect


async def get_all_links(
    type: bool | None = None, offset_min: int = 0, offset_max: int = 30
) -> Tuple[List[URLInfo], int]:
    """Получение всех ссылок по заданным параметрам

    Args:
        type (bool | None, optional): какие ссылки показывать(все/активные/неактивные). Defaults to None.
        offset_min (int, optional): откуда начинать выборку. Defaults to 0.
        offset_max (int, optional): где заканчивать выборку. Defaults to 30.

    Returns:
        Tuple[List[URLInfo], int]: список ссылок полученных и общее число ссылок по заданным параметрам
    """
    if type is None:
        links = await URLInfo.all()
    else:
        links = await URLInfo.all().filter(is_active=type)
    links.sort(key=lambda x: x.id)

    return links[offset_min:offset_max], len(links)


async def get_orig_link(short_link: str) -> URLInfo | None:
    """Получение оригинальной ссылки по короткой

    Args:
        short_link (str): короткая ссылка

    Returns:
        URLInfo | None: оригинальная ссылка, если она есть в базе данных
    """
    res = await URLInfo.get_or_none(link=short_link, is_active=True)
    if not res:
        return None

    return res


async def change_activate_status(short_link: str) -> bool:
    """Изменение активности ссылки

    Args:
        short_link (str): ссылка, у которой нужно изменить параметр

    Returns:
        bool: True, если ссылка есть и активность изменена. False, если ссылки нет в базе данных
    """
    url = await URLInfo.get_or_none(link=short_link)
    if not url or not url.is_active:
        return False

    url.is_active = False
    await url.save()

    return True


async def change_statistic(short_link: str):
    """Запись времени клика по ссылке(перехода)

    Args:
        short_link (str): короткая ссылка
    """
    url = await URLInfo.get(link=short_link)
    await URLRedirect.create(url_id=url.id)


async def get_stats(link_id: int) -> Dict[str, int]:
    """Получение статистики за час и день у ссылки

    Args:
        link_id (int): ID ссылки, у которой нужно получить статистику

    Returns:
        Dict[str, int]: данные статистики
    """
    now = datetime.now(timezone.utc)

    hour_stats = await URLRedirect.filter(
        url_id=link_id, clicked_at__gte=now - timedelta(hours=1)
    ).count()

    day_stats = await URLRedirect.filter(
        url_id=link_id, clicked_at__gte=now - timedelta(days=1)
    ).count()

    return {"hour_stats": hour_stats, "day_stats": day_stats}


async def write_short_link(original_link: str, short_link: str, due_date: datetime) -> bool:
    """Запись данных короткой ссылки в базу данных

    Args:
        original_link (str): оригинальная ссылка
        short_link (str): короткая(сгенерированная) ссылка
        due_date (datetime): время истечения активности

    Returns:
        bool: создана запись или нет
    """
    try:
        await URLInfo.create(original_link=original_link, link=short_link, due_date=due_date)
        return True
    except Exception as e:
        print(f"\033[031mERROR:\t  {e}\033[0m]")
        return False


async def change_expired_links_status():
    """Проверка актуальности активных ссылок(для Apscheduler)"""
    print(f"\033[034mCRON:\033[0m\t  {datetime.now(timezone.utc)}")
    await URLInfo.filter(is_active=True, due_date__lt=datetime.now(timezone.utc)).update(
        is_active=False
    )
