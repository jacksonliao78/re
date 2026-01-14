from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserCreate, UserLogin, UserResponse, Token
from app.dependencies import get_current_user
from app.db.models import User
import uuid
from app.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

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
    return UserResponse( id=str(current_user.id), email = current_user.email)

