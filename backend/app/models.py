from pydantic import BaseModel
from typing import Optional


class Job(BaseModel):
    id: str
    title: str
    position_level: Optional[str] = None
    description: str
    company: Optional[str] = None
    location: Optional[str] = None
    url: str


class SearchQuery(BaseModel):
    type: str
    level: list[str]


class Heading(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class EducationEntry(BaseModel):
    school: Optional[str] = None
    location: Optional[str] = None
    degree: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    details: list[str] = []


class Project(BaseModel):
    name: Optional[str] = None
    description: list[str] = []
    tech: Optional[list[str]] = None
    dateRange: Optional[str] = None


class Resume(BaseModel):
    heading: Optional[Heading] = None
    summary: Optional[str] = None
    languages: Optional[list[str]] = None
    technologies: Optional[list[str]] = None
    education: Optional[list[EducationEntry]] = None
    experience: Optional[list[Experience]] = None
    projects: Optional[list[Project]] = None

    def to_string(self) -> str:
        parts: list[str] = []

        if self.heading:
            name = self.heading.name or ""
            contact_bits: list[str] = []
            if self.heading.phone:
                contact_bits.append(self.heading.phone)
            if self.heading.email:
                contact_bits.append(self.heading.email)
            if self.heading.location:
                contact_bits.append(self.heading.location)
            heading_line = name.strip()
            if contact_bits:
                heading_line = f"{heading_line} – " + " | ".join(contact_bits)
            if heading_line.strip():
                parts.append(heading_line.strip())

        if self.summary:
            parts.append(self.summary.strip())

        if self.languages:
            parts.append("\nLanguages:")
            for lang in self.languages:
                parts.append(f"- {lang}")

        if self.technologies:
            parts.append("\nTechnologies:")
            for tech in self.technologies:
                parts.append(f"- {tech}")

        if self.education:
            parts.append("\nEducation:")
            for edu in self.education:
                line_bits: list[str] = []
                if edu.degree:
                    line_bits.append(edu.degree)
                if edu.school:
                    line_bits.append(f"at {edu.school}")
                if edu.location:
                    line_bits.append(f"({edu.location})")
                if edu.start or edu.end:
                    dates = " - ".join(
                        [d for d in [edu.start or "", edu.end or ""] if d]
                    )
                    if dates:
                        line_bits.append(dates)
                if line_bits:
                    parts.append(f"- {' '.join(line_bits)}")

        if self.experience:
            parts.append("\nExperience:")
            for exp in self.experience:
                exp_parts: list[str] = []
                if exp.title:
                    exp_parts.append(exp.title)
                if exp.company:
                    exp_parts.append(f"at {exp.company}")
                if exp.location:
                    exp_parts.append(f"({exp.location})")
                if exp.start or exp.end:
                    dates = " - ".join(
                        [d for d in [exp.start or "", exp.end or ""] if d]
                    )
                    if dates:
                        exp_parts.append(dates)

                if exp_parts:
                    parts.append(f"- {' '.join(exp_parts)}")

                for detail in exp.details:
                    text = detail.strip()
                    if text:
                        parts.append(f"  • {text}")

        if self.projects:
            parts.append("\nProjects:")
            for proj in self.projects:
                header_bits: list[str] = []
                if proj.name:
                    header_bits.append(proj.name)
                if proj.dateRange:
                    header_bits.append(f"({proj.dateRange})")
                if header_bits:
                    parts.append(f"- {' '.join(header_bits)}")
                for desc in proj.description:
                    text = desc.strip()
                    if text:
                        parts.append(f"  • {text}")
                if proj.tech:
                    parts.append(f"  Tech: {', '.join(proj.tech)}")

        return "\n".join(parts).strip()


class Suggestion(BaseModel):
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
