
from pydantic import BaseModel


class Job( BaseModel ):
    title: str
    position_level: str
    description: list[ str ]
    company: str
    location: str
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
    ...


#db stuff