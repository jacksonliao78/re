from fastapi import APIRouter
from pydantic import BaseModel
from scraper import scrape
from models import Job
from models import SearchQuery

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/search")
async def findJobs(q: SearchQuery) -> list[Job]:
    
    if not q or not getattr(q, "type", None):
        return []
    return await scrape(q)

