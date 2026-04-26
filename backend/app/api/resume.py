from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.parse import parse
from app.tailor import tailor_resume_with_rag
from app.latex_resume import render_resume_pdf
from app.models import Job, Resume, KnowledgeDocumentIn
from app.database import get_db
from app.dependencies import get_current_user_optional, get_current_user
from app.db.models import User
from app.rag import ingest_user_knowledge, list_user_knowledge_documents


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
async def tailorResume(
    resume: Resume,
    job: Job,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    """Generate tailoring suggestions for a resume given a job."""
    user_id = current_user.id if current_user else None
    suggestions = tailor_resume_with_rag(resume=resume, job=job, db=db, user_id=user_id)
    return JSONResponse(
        status_code=200, content=[s.model_dump() for s in suggestions]
    )


@router.post("/knowledge")
async def create_knowledge_doc(
    body: KnowledgeDocumentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not body.content.strip():
        raise HTTPException(status_code=400, detail="content is required")
    doc, chunk_count = ingest_user_knowledge(
        db=db,
        user_id=current_user.id,
        title=body.title,
        content=body.content,
        source_type=body.sourceType or "note",
    )
    return {
        "id": str(doc.id),
        "title": doc.title,
        "sourceType": doc.source_type,
        "chunkCount": chunk_count,
    }


@router.get("/knowledge")
async def get_knowledge_docs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_knowledge_documents(db=db, user_id=current_user.id)


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
