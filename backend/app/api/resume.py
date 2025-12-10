from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi.responses import JSONResponse
from parse import parse

router = APIRouter( prefix="/resume", tags=["Resume"] )

# Shoud be a PDF at this point
@router.post('/upload')
async def uploadResume( file: UploadFile ):

    if not file.filename.endswith(".pdf"):
        return JSONResponse( status_code=400, content={"message": "Requires .pdf ending"})
    
    resume = await parse( file.read() )
    

    #put it in a DB ? later prob


    #just need to return the resume so the frontend can display it
    
    return JSONResponse( status_code=200 )


# tailors a resume based on a job
@router.post('/tailor')
def tailorResume():

    #llm integration
    #important stuff here probably

    return

@router.post('/finish')
def finishTailoring():


    #put job in ignored
    return