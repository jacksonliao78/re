import pytest

from app.models import Job, Resume
from app.tailor import tailor_resume
from app.parse import parse
from pathlib import Path

job_data = {
    "id": "1",
    "title": "Senior Backend Engineer",
    "position_level": "Senior",
    "description": (
        "Acme Corp is hiring a Senior Backend Engineer to design and build scalable backend services. "
        "You will design RESTful APIs, build distributed systems, improve latency and reliability, "
        "and mentor junior engineers. Required skills: Python, FastAPI, Docker, Kubernetes, PostgreSQL, "
        "and experience with distributed systems. Nice to have: Elasticsearch, gRPC, AWS (EKS), Prometheus/Grafana."
    ),
    "company": "Acme Corp",
    "location": "San Francisco, CA",
    "url": "https://acme.example.com/jobs/12345"
}

job = Job(**job_data)

pdf_path = Path(__file__).parent / "resources" / "random.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

text = parse(pdf_bytes)
suggestions = tailor_resume(text, job)  # returns list[Suggestion]
for s in suggestions:
    print(s.model_dump())
