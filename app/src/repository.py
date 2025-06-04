from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple

from app.src.db.models import URLInfo, URLRedirect


async def get_all_links(
    type: bool | None = None, offset_min: int = 0, offset_max: int = 30
) -> Tuple[List[URLInfo], int]:
    if type is None:
        links = await URLInfo.all()
    else:
        links = await URLInfo.all().filter(is_active=type)
    links.sort(key=lambda x: x.id)
    return links[offset_min:offset_max], len(links)


async def get_orig_link(short_link: str) -> URLInfo | None:
    res = await URLInfo.get_or_none(link=short_link, is_active=True)
    if not res:
        return None

    return res


async def change_activate_status(short_link: str) -> bool:
    url = await URLInfo.get_or_none(link=short_link)
    if not url or not url.is_active:
        return False
    url.is_active = False
    await url.save()
    return True


async def change_statistic(short_link: str):
    url = await URLInfo.get(link=short_link)
    await URLRedirect.create(url_id=url.id)


async def get_stats(link_id: int) -> Dict[str, int]:
    now = datetime.now(timezone.utc)
    hour_stats = await URLRedirect.filter(
        url_id=link_id, clicked_at__gte=now - timedelta(hours=1)
    ).count()
    day_stats = await URLRedirect.filter(
        url_id=link_id, clicked_at__gte=now - timedelta(days=1)
    ).count()

    return {"hour_stats": hour_stats, "day_stats": day_stats}


async def write_short_link(original_link: str, short_link: str, due_date: datetime) -> bool:
    try:
        await URLInfo.create(original_link=original_link, link=short_link, due_date=due_date)
        return True
    except Exception as e:
        print(f"\033[031mERROR:\t  {e}\033[0m]")
        return False

async def change_expired_links_status():
    print(f"\033[034mCRON:\033[0m\t  {datetime.now(timezone.utc)}")
    await URLInfo.filter(is_active=True, due_date__lt=datetime.now(timezone.utc)).update(is_active=False)