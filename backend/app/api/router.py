from fastapi import APIRouter
from app.api.jobs import router as jobrouter
from app.api.resume import router as resumerouter
from app.api.auth import router as authrouter

router = APIRouter()
router.include_router(authrouter)
router.include_router(jobrouter)
router.include_router(resumerouter)