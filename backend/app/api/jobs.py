from fastapi import APIRouter
from pydantic import BaseModel
from scraper import scrape
from models import Job
from models import SearchQuery

router = APIRouter( prefix= "/jobs", tags=["Jobs"] )


query = SearchQuery() #just one search query for everybody for now 

@router.post("/updateQuery")
def updateQuery( type: str, level: list[str] ):
    global query
    query.type = type
    query.level = level
    return True

@router.get("/search")
async def findJobs( query: SearchQuery ) -> list[ Job ]:
    if( query == None ):
        return [] 
    return await scrape( query )
    #returns a list of ~10 (or as many as the webscraper can find)

