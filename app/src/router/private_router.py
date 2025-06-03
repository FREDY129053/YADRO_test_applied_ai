from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import app.src.services as URLService
from app.src.schemas import (
    CreateShortLink,
    DeactivateShortLink,
    LinkInfo,
    Message,
    StatisticLinkInfo,
)

security = HTTPBasic()
private_router = APIRouter(prefix="/private", tags=["Private Endpoints"])


@private_router.get("/all_links", response_model=Message[LinkInfo])
async def get_all_links(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    filter: Annotated[Literal["all", "active", "inactive"], Query()] = "all",
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, default=30),
):
    return await URLService.get_all_links(filter=filter, page=page, size=size)


@private_router.get("/links_stats", response_model=Message[StatisticLinkInfo])
async def get_links_stats(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, default=30),
):
    return await URLService.get_stats(page=page, size=size)


@private_router.post("/generate_link")
async def generate_short_url(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], data: CreateShortLink
):
    created = await URLService.generate_url(data.url)
    if not created:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot create link")

    return JSONResponse(content={"message": created}, status_code=status.HTTP_201_CREATED)


@private_router.put("/deactivate")
async def deactivate_link(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], data: DeactivateShortLink
):
    result = await URLService.deactivate_link(data.short_url)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="cannot find this active link"
        )

    return JSONResponse(
        content={"message": "link deactivated"},
    )
