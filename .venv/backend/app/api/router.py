from fastapi import APIRouter
from api.jobs import router as jobrouter
from api.resume import router as resumerouter

router = APIRouter()
router.include_router( jobrouter )
router.include_router( resumerouter )