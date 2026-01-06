from fastapi import APIRouter
from api.jobs import router as jobrouter
from api.resume import router as resumerouter
from api.auth import router as authrouter

router = APIRouter()
router.include_router( authrouter )
router.include_router( jobrouter )
router.include_router( resumerouter )