from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import SignupRequest, LoginRequest, TokenResponse

router = APIRouter()


@router.post("/auth/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth = AuthService()

    existing = user_repo.get_by_email(request.email)
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user_repo.create(User(
        email=request.email,
        hashed_password=auth.hash_password(request.password),
        full_name=request.full_name,
    ))

    token = auth.create_access_token(str(new_user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth = AuthService()

    user = user_repo.get_by_email(form_data.username)
    if user is None or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth.create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}