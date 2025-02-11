from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from schemas.user import UserUpdate

router = APIRouter()



@router.get("/users")
async def get_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: str = Query(None)
):
    query = db.query(User)
    
    if search:
        query = query.filter(User.username.contains(search) | User.email.contains(search))
    
    users = query.offset(skip).limit(limit).all()
    
    return [{'username': user.username, 'email': user.email, 'is_active': user.is_active, 'id': user.id} for user in users]
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

