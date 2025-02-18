from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from passlib.context import CryptContext
from schemas.user import userCreate, userLogin
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
import os

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")
        return {
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    except JWTError:
        print("JWTError")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/signup")
async def signup(user: userCreate, db: Session = Depends(get_db)):
    print(user.username, user.email, user.password)
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login")
async def login(form_data: userLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "is_admin": user.is_admin}

