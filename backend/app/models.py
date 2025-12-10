
from pydantic import BaseModel
from typing import Optional


class Job( BaseModel ):
    title: str
    position_level: Optional[str] = None
    description: str 
    company: Optional[str] = None
    location: Optional[str] = None # should be city and state ideally
    url: str
    #whatever other attributes a job might have

class SearchQuery( BaseModel ):
    type: str  #can change to list maybe
    level: list[ str ]



# A resume may have some of the following
# a brief paragraph
# experience
# projects
# skills
class Resume( BaseModel ):
    summary: Optional[str] = None
    experience: Optional[list[str]] = None
    projects: Optional[list[str]] = None
    skills: Optional[list[str]] = None


#suggestion class?

#db stuff