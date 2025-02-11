from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Trainer
from schemas.trainers import TrainerCreate, TrainerUpdate

router = APIRouter()

@router.get("/trainers")
async def get_trainers(db: Session = Depends(get_db)):
    trainers = db.query(Trainer).limit(10).all()
    return [{"name": trainer.name, "specialization": trainer.specialization, "contact_info": trainer.contact} for trainer in trainers]

@router.get("/trainers/{trainer_id}")
async def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer

@router.post("/trainers")
async def create_trainer(trainer: TrainerCreate, db: Session = Depends(get_db)):
    new_trainer = Trainer(
        name=trainer.name,
        specialization=trainer.specialization,
        contact=trainer.contact
    )
    db.add(new_trainer)
    db.commit()
    return {}