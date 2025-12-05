from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter( prefix= "/jobs", tags=["Jobs"] )

class Job( BaseModel ):
    name: str
    #whatever other attributes a job has

class SearchQuery( BaseModel ):
    type: list[ str ]
    level: list[ str ]

@router.get("/search")
async def findJobs():


    print("s")