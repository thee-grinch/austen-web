from database.models import User
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

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
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/dashboard")
async def get_dashboard_data(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "stats": {
            "workouts_completed": 15,
            "calories_burned": 4500,
            "weight_lost": 3.2
        },
        "recent_activities": ["Morning Run", "Strength Training"]
    }

@router.get("/metrics")
async def get_metrics(current_user: User = Depends(get_current_user)):
    return [
            {
                "title": "Total Workouts",
                "value": "32",
                "icon": "fas fa-dumbbell"
            },
            {
                "title": "Calories Burned",
                "value": "4,500",
                "icon": "fas fa-fire"
            },
            {
                "title": "Active Minutes",
                "value": "480",
                "icon": "fas fa-clock"
            },
            {
                "title": "Weight Progress",
                "value": "-3.2 kg",
                "icon": "fas fa-weight"
            }
        ]
@router.get("/progress")
async def get_progress():
# async def get_progress(current_user: User = Depends(get_current_user)):
    return {
        "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "datasets": [
            {
                "label": "Weight Lost",
                "data": [1.2, 0.8, 0.5, 0.7],
                "borderColor": "#FF6B35",
                "tension": 0.4
            },
            {
                "label": "Calories Burned",
                "data": [250, 300, 200, 400],
                "borderColor": "#4CAF50",
                "tension": 0.4
            }
        ]
    }

@router.get('/programs')
async def get_programs():
    return [
        {
            "name": "Weight Loss Program",
            "description": "A 4-week program to help you lose weight",
            "progress": 80,

        },
        {
            "name": "Strength Training",
            "description": "A 6-week program to help you build muscle",
            "progress": 0.3
        },
        {
            "name": "Cardio Training",
            "description": "A 12-week program to help you run a marathon",
            "progress": 0.1
        },
        {
            "name": "Yoga for Beginners",
            "description": "A 2-week program to help you get started with yoga",
            "progress": 0.8
        }
    ]
