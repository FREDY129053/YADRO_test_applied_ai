from fastapi import APIRouter, HTTPException, status
from starlette.responses import RedirectResponse

import app.src.services as URLService

public_router = APIRouter(tags=["Public Endpoints"])


@public_router.get("/{short_url}")
async def follow_the_link(short_url: str):
    original_link = await URLService.get_original_url(short_link=short_url)
    if not original_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="cannot find active link!"
        )
    response = RedirectResponse(url=original_link)

    return response
