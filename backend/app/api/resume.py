from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.parse import parse
from app.tailor import tailor_resume
from app.models import Job, Resume
from app.latex_resume import render_resume_pdf


router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def uploadResume(file: UploadFile):
    """Upload a PDF resume and return the parsed structured Resume."""
    if not file.filename.endswith(".pdf"):
        return JSONResponse(
            status_code=400, content={"message": "Requires .pdf ending"}
        )

    contents = await file.read()
    resume = parse(contents)
    await file.close()

    return JSONResponse(status_code=200, content=resume.model_dump())


@router.post("/tailor")
async def tailorResume(resume: Resume, job: Job):
    """Generate tailoring suggestions for a resume given a job."""
    suggestions = tailor_resume(resume, job)
    return JSONResponse(
        status_code=200, content=[s.model_dump() for s in suggestions]
    )


@router.post("/render-pdf")
async def render_resume(resume: Resume):
    """
    Render the given structured Resume into Jake's LaTeX template and return a PDF.
    """
    try:
        pdf_bytes = render_resume_pdf(resume)
    except RuntimeError as exc:
        return JSONResponse(
            status_code=500,
            content={"message": f"Failed to render resume PDF: {exc}"},
        )

    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="resume.pdf"'},
    )
