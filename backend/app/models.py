
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

    def toString( self ) -> str:
        resume = ""
        if( self.summary ): resume += "Summary: \n" + self.summary + "\n"
        if( self.experience ):
            resume += "Experience: \n" 
            for i in range( len(self.experience) ):
                resume += i + "\n" + self.experience[i] + "\n" 
        if( self.projects ): 
            resume += "Projects: \n"
            for i in range( len(self.projects) ):
                resume += i + "\n" + self.projects[i] + "\n"
        if( self.skills ):
            resume += "Skills: \n"
            for skill in self.skills:
                resume += skill
        return resume


class Suggestion( BaseModel ):
    section: str
    original: str
    updated: str
    explanation: str

#db stuff