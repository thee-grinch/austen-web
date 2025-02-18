from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from schemas.user import UserUpdate

router = APIRouter()




@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.dict()

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = user_data.username
    user.email = user_data.email
    user.is_active = user_data.is_active
    db.commit()
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.patch("/users/{user_id}/status")
async def patch_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = user_data.is_active
    db.commit()
    return {"message": "User status updated successfully"}

@router.get("/detailed-progress")
async def get_detailed_progress(db: Session = Depends(get_db)):
    """this returns the progress of the user"""
    return {
        "type": "bar",
        "labels": ["January", "February", "March", "April", "May", "June", "July"],
        "datasets": [
            {
                "label": "Weight",
                "data": [65, 64, 63, 62, 61, 60, 59],
                "borderColor": "rgba(255, 107, 53, 1)",
                "backgroundColor": "rgba(255, 107, 53, 0.2)",
                "fill": True
            },
            {
                "label": "Body Fat Percentage",
                "data": [20, 19, 18, 17, 16, 15, 14],
                "borderColor": "rgba(76, 175, 80, 1)",
                "backgroundColor": "rgba(76, 175, 80, 0.2)",
                "fill": True
            }
        ]
    }


