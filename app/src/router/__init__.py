from fastapi import APIRouter
from .private_router import private_router
from .public_router import public_router

router = APIRouter()

router.include_router(public_router)
router.include_router(prefix="/api", router=private_router)