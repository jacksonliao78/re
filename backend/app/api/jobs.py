from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.scraper import scrape
from app.models import Job, SearchQuery
from app.database import get_db
from app.dependencies import get_current_user_optional
from app.db.models import User, IgnoredJob

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/search")
async def find_jobs(
    q: SearchQuery,
    current_user: User | None = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
) -> list[Job]:
    if not q or not getattr(q, "type", None):
        return []
    jobs = await scrape(q)
    if not current_user:
        return jobs
    ignored = {r[0] for r in db.query(IgnoredJob.job_id).filter(IgnoredJob.user_id == current_user.id).all()}
    return [j for j in jobs if j.id not in ignored]

