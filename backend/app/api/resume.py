from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi.responses import JSONResponse
from parse import parse
from tailor import tailor_resume
from models import Job, Resume

router = APIRouter( prefix="/resume", tags=["Resume"] )

# Shoud be a PDF at this point
@router.post('/upload')
async def uploadResume( file: UploadFile ):

    if not file.filename.endswith(".pdf"):
        return JSONResponse( status_code=400, content={"message": "Requires .pdf ending"})
    
    contents = await file.read()
    
    resume = parse( contents )

    file.close()
    

    #put it in a DB ? later prob


    #just need to return the resume so the frontend can display it
    
    return JSONResponse( status_code=200 )


# tailors a resume based on a job
@router.post('/tailor')
async def tailorResume( resume: Resume, job: Job ):

    suggestions = await tailor_resume( resume, job )

    return suggestions #todo json

@router.post('/finish')
def finishTailoring():


    #put job in ignored
    return