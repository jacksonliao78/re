
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


# A resume may have some of the following
# a brief paragraph
# experience
# projects
# skills
class Resume(BaseModel):
    summary: Optional[str] = None
    skills: Optional[list[str]] = None
    experience: Optional[list[list[str]]] = None
    projects: Optional[list[list[str]]] = None

    def to_string(self) -> str:
        parts: list[str] = []

        if self.summary:
            parts.append(self.summary.strip())

        if self.skills:
            parts.append("\nSkills:")
            for skill in self.skills:
                parts.append(f"- {skill}")

        if self.experience:
            parts.append("\nExperience:")
            for entry in self.experience:
                for bullet in entry:
                    text = bullet.strip()
                    if text:
                        parts.append(f"- {text}")

        if self.projects:
            parts.append("\nProjects:")
            for entry in self.projects:
                for bullet in entry:
                    text = bullet.strip()
                    if text:
                        parts.append(f"- {text}")

        return "\n".join(parts).strip()


class Suggestion( BaseModel ):
    section: str
    entryIdx: Optional[str]
    bulletIdx: Optional[str]
    original: str
    updated: str
    explanation: str

#db stuff