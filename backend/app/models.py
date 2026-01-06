
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
    type: str
    level: list[str]

class Experience( BaseModel ):
    company: Optional[str] = None
    title: Optional[str] = None
    details: list[str] = []

class Project( BaseModel ):
    name: Optional[str] = None
    description: list[str] = []
    tech: Optional[list[str]] = None

# A resume may have some of the following
# a brief paragraph
# experience
# projects
# skills
class Resume(BaseModel):
    summary: Optional[str] = None
    skills: Optional[list[str]] = None
    experience: Optional[list[Experience]] = None
    projects: Optional[list[Project]] = None

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
            for exp in self.experience:
                # Build experience header
                exp_parts = []
                if exp.title:
                    exp_parts.append(exp.title)
                if exp.company:
                    exp_parts.append(f"at {exp.company}")
                
                if exp_parts:
                    parts.append(f"- {' '.join(exp_parts)}")
                
                # Add details
                for detail in exp.details:
                    text = detail.strip()
                    if text:
                        parts.append(f"  • {text}")

        if self.projects:
            parts.append("\nProjects:")
            for proj in self.projects:
                # Project name/header
                if proj.name:
                    parts.append(f"- {proj.name}")
                # Add description bullets
                for desc in proj.description:
                    text = desc.strip()
                    if text:
                        parts.append(f"  • {text}")
                # Add tech stack if available
                if proj.tech:
                    parts.append(f"  Tech: {', '.join(proj.tech)}")

        return "\n".join(parts).strip()


class Suggestion( BaseModel ):
    section: str
    entryIdx: Optional[int] = None
    bulletIdx: Optional[int] = None
    original: str
    updated: str
    explanation: str

# Auth models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str