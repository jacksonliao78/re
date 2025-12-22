
from pydantic import BaseModel
from typing import Optional


class Job( BaseModel ):
    id: str
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

    def to_string(self) -> str:
        
        parts: list[str] = []

        if self.summary:
            parts.append(self.summary.strip())

        if self.skills:
            for skill in self.skills:
                parts.append( skill + "  " )

        if self.experience:
            parts.append("\nExperience:")
            for item in self.experience:

                if isinstance(item, dict):
                    title = item.get("title") or item.get("company") or ""
                    details = item.get("details") or ""
                    if title and details:
                        parts.append(f"- {title}: {details}")
                    elif details:
                        parts.append(f"- {details}")
                    elif title:
                        parts.append(f"- {title}")
                else:
                    text = str(item).strip()
                    if text:
                        parts.append(f"- {text}")

        if self.projects:

            parts.append("\nProjects:")
            for item in self.projects:

                if isinstance(item, dict):
                    name = item.get("name") or ""
                    desc = item.get("description") or ""
                    if name and desc:
                        parts.append(f"- {name}: {desc}")
                    elif desc:
                        parts.append(f"- {desc}")
                    elif name:
                        parts.append(f"- {name}")
                else:
                    text = str(item).strip()
                    if text:
                        parts.append(f"- {text}")

        return "\n".join(parts).strip()

    def __str__(self) -> str:
        return self.to_string()



class Suggestion( BaseModel ):
    section: str
    entryIdx: Optional[str]
    bulletIdx: Optional[str]
    original: str
    updated: str
    explanation: str

#db stuff