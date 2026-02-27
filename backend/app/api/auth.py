from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import UserCreate, UserLogin, UserResponse, Token, Resume
from app.dependencies import get_current_user
from app.db.models import User, IgnoredJob
import uuid
from app.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


class IgnoredJobAdd(BaseModel):
    job_id: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):

    #check if there's a user with that info
    existing = db.query(User).filter(User.email == user_data.email).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash( user_data.password )
    new_user = User( id = uuid.uuid4(), email = user_data.email, password_hash = hashed_password )
    
    db.add( new_user )
    db.commit()
    db.refresh( new_user )

    return UserResponse( id = str(new_user.id), email = new_user.email )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password( user_data.password, user.password_hash ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(data = {"sub": str(user.id)})
    
    return Token( access_token= token, token_type = "bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(id=str(current_user.id), email=current_user.email)


# Default resume (the "original" resume to reset to when rechoosing a job)
@router.get("/me/default-resume")
async def get_default_resume(current_user: User = Depends(get_current_user)):
    if current_user.default_resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No default resume")
    return current_user.default_resume


@router.put("/me/default-resume")
async def put_default_resume(resume: Resume, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.default_resume = resume.model_dump()
    db.commit()
    return current_user.default_resume


# Ignored jobs (filtered out of scrape results for this user)
@router.get("/me/ignored-jobs")
async def get_ignored_jobs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(IgnoredJob.job_id).filter(IgnoredJob.user_id == current_user.id).all()
    return [r[0] for r in rows]


@router.post("/me/ignored-jobs")
async def add_ignored_job(body: IgnoredJobAdd, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job_id = (body.job_id or "").strip()[:64]
    if not job_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="job_id required")
    existing = db.query(IgnoredJob).filter(IgnoredJob.user_id == current_user.id, IgnoredJob.job_id == job_id).first()
    if existing:
        return {"job_id": job_id, "ignored": True}
    db.add(IgnoredJob(user_id=current_user.id, job_id=job_id))
    db.commit()
    return {"job_id": job_id, "ignored": True}

