import io
import os
import json
import re

from app.models import (
    Resume,
    Heading,
    EducationEntry,
    Experience,
    Project,
)
from app.prompts import parse_prompts, parse_schema_examples
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI


try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def parse(file: bytes) -> Resume:
    stream = io.BytesIO(file)
    reader = PdfReader(stream)
    page = reader.pages[0]

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set.\n"
            "Set it locally with: export GOOGLE_API_KEY=your_key\n"
            "Or create a .env file with: GOOGLE_API_KEY=your_key"
        )

    # temp 0 to encourage deterministic output.
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", retries=2, api_key=api_key, temperature=0
    )

    page_text = page.extract_text()

    # three consolidated prompts: heading+education, experience+projects, summary+skills
    keys = ["heading_education", "experience_projects", "summary_skills"]

    
    parsed_outputs: dict[str, dict | None] = {}

    for key, prompt in zip(keys, parse_prompts):
        output_instructions = (
            "IMPORTANT: Reply with valid JSON only and nothing else. "
            "Do NOT include any explanatory text, markdown, or backticks. "
            "The JSON must match the schema example below exactly (use the same keys):\n"
            + json.dumps(parse_schema_examples[key], indent=2)
        )

        system_prompt = prompt + output_instructions
        message = [("system", system_prompt), ("user", page_text)]

        res = model.invoke(message)  # actual AI call
        raw = getattr(res, "text", str(res))

        # try to parse JSON directly, or substring if possible
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            # first JSON
            m = re.search(r"(\{.*\}|\[.*\])", raw, re.S)
            if m:
                try:
                    parsed = json.loads(m.group(1))
                except Exception:
                    parsed = None

        if parsed is None:
            print(f"failed to parse JSON for {key}")
            parsed_outputs[key] = None
        else:
            parsed_outputs[key] = parsed

    heading_education = parsed_outputs.get("heading_education") or {}
    experience_projects = parsed_outputs.get("experience_projects") or {}
    summary_skills = parsed_outputs.get("summary_skills") or {}

    resume = Resume()

    # heading
    heading_data = heading_education.get("heading") or None
    if isinstance(heading_data, dict) and heading_data:
        resume.heading = Heading(
            name=heading_data.get("name"),
            phone=heading_data.get("phone"),
            email=heading_data.get("email"),
            location=heading_data.get("location"),
            linkedin=heading_data.get("linkedin"),
            github=heading_data.get("github"),
        )

    # education
    education_list = heading_education.get("education") or []
    if isinstance(education_list, list) and education_list:
        resume.education = []
        for edu_data in education_list:
            if not isinstance(edu_data, dict):
                continue
            edu = EducationEntry(
                school=edu_data.get("school"),
                location=edu_data.get("location"),
                degree=edu_data.get("degree"),
                start=edu_data.get("start"),
                end=edu_data.get("end"),
            )
            resume.education.append(edu)
        if not resume.education:
            resume.education = None

    # languages and technologies (do not parse summary for now)
    if isinstance(summary_skills, dict):
        languages = summary_skills.get("languages")
        if isinstance(languages, list) and languages:
            resume.languages = languages
        else:
            resume.languages = None

        technologies = summary_skills.get("technologies")
        if isinstance(technologies, list) and technologies:
            resume.technologies = technologies
        else:
            resume.technologies = None

    # experience
    experience_list = experience_projects.get("experience") or []
    if isinstance(experience_list, list) and experience_list:
        resume.experience = []
        for exp_data in experience_list:
            if not isinstance(exp_data, dict):
                continue
            exp = Experience(
                company=exp_data.get("company"),
                title=exp_data.get("title"),
                location=exp_data.get("location"),
                start=exp_data.get("start"),
                end=exp_data.get("end"),
                details=exp_data.get("details") or [],
            )
            resume.experience.append(exp)
        if not resume.experience:
            resume.experience = None

    # projects
    projects_list = experience_projects.get("projects") or []
    if isinstance(projects_list, list) and projects_list:
        resume.projects = []
        for proj_data in projects_list:
            if not isinstance(proj_data, dict):
                continue
            proj = Project(
                name=proj_data.get("name"),
                description=proj_data.get("description") or [],
                tech=proj_data.get("tech"),
                dateRange=proj_data.get("dateRange"),
            )
            resume.projects.append(proj)
        if not resume.projects:
            resume.projects = None

    print(resume.to_string())

    return resume


# pdf_path = Path(__file__).parent / "tests" / "resources" / "random.pdf"

# with open(pdf_path, "rb") as f:
#     pdf_bytes = f.read()
# text = parse(pdf_bytes)
