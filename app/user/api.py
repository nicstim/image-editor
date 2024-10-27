from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta


from app.config import settings
from app.models import User, UserTask
from app.user.schemas import UserCreate, UserResponse, Token, UserLogin, UserInfo
from app.utils.jwt_utils import create_access_token, get_current_user
from app.utils.password_utils import hash_password, verify_password
from app.utils.db_utils import get_db

router = APIRouter()


@router.post("/registration/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        id=str(uuid4()),
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        access_token=create_access_token(
            data={"email": user.email},
            expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ))


@router.post("/login/", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": db_user.email}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserInfo)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/history/{user_id}/")
def get_user_history(user_id: str, db: Session = Depends(get_db)):
    return db.query(UserTask).filter(UserTask.user_id == user_id).all()
