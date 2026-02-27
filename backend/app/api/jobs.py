from fastapi import APIRouter
from pydantic import BaseModel
from app.scraper import scrape
from app.models import Job, SearchQuery

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/search")
async def findJobs( q: SearchQuery ) -> list[Job]:
    
    if not q or not getattr( q, "type", None ):
        return []
    return await scrape( q )

