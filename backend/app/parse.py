import io
import os
import json
import re

from backend.app.models import Resume
from backend.app.prompts import parse_prompts
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import File
from pathlib import Path


try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def parse( file: bytes ) -> Resume:


    stream = io.BytesIO( file )
    reader = PdfReader( stream )
    page = reader.pages[0]

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set.\n"
            "Set it locally with: export GOOGLE_API_KEY=your_key\n"
            "Or create a .env file with: GOOGLE_API_KEY=your_key"
        )

    
    # temp 0 to encourage deterministic output.
    model = ChatGoogleGenerativeAI( model="gemini-2.5-flash", retries=2, api_key=api_key, temperature=0 ) 

    parsed_outputs = {}
    keys = [ "summary", "skills", "experience", "projects" ]

    page_text = page.extract_text()

    schema_examples = {
            0: {"summary": "A short 2-3 sentence professional summary."},
            1: {"skills": ["python", "machine learning", "aws"]},
            2: {"experience": [{"company": "Example Co", "title": "SWE", "start": "YYYY-MM", "end": "YYYY-MM or Present", "details": ["Developed X", "Used Y", "Found Z"]}]},
            3: {"projects": [{"name": "Project Name", "description": ["Built X", "Incorporated Y"], "tech": ["python"]}]}
        }

    for i in range(len(parse_prompts)):

        output_instructions = (
            "IMPORTANT: Reply with valid JSON only and nothing else. Do NOT include any explanatory text, markdown, or backticks. The JSON must match the schema example below exactly (use the same keys):\n"
            + json.dumps(schema_examples[i], indent=2)
        )

        system_prompt = parse_prompts[i] + output_instructions

        message = [ ("system", system_prompt), ("user", page_text) ]

        res = model.invoke(message) # actual AI call

        raw = getattr(res, "text", str(res))

        # try to parse JSON directly, or substring if possible 
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            # first JSON 
            m = re.search( r"(\{.*\}|\[.*\])", raw, re.S ) #regex
            if m:
                try:
                    parsed = json.loads(m.group(1))
                except Exception:
                    parsed = None

        if parsed is None:
            print("failed to parse JSON")
            parsed_outputs[ keys[i] ] = None
        else:
            parsed_outputs[ keys[i] ] = parsed
            #print(f"Parsed {keys[i]}:")
            #print(json.dumps(parsed, indent=2))


    summary = parsed_outputs.get("summary")
    skills = parsed_outputs.get("skills")
    experience = parsed_outputs.get("experience")
    projects = parsed_outputs.get("projects")

    resume = Resume()
    resume.summary = summary.get("summary") if summary else None
    resume.skills = skills.get("skills") if skills else None
    resume.experience = [ exp.get("details", "") for exp in experience.get("experience", []) ] if experience else None
    resume.projects = [ proj.get("description", "") for proj in projects.get("projects", []) ] if projects else None

    

    print( resume.to_string() )

    return resume


#pdf_path = Path(__file__).parent / "tests" / "resources" / "random.pdf"

#with open(pdf_path, "rb") as f:
  #  pdf_bytes = f.read()

#text = parse(pdf_bytes)