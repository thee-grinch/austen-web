
from database.database import SessionLocal
from database.models import Metric, Progress, Program, Workout, Trainer, Feedback, User
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserUpdate
from schemas.workouts import TrainerCreate, WorkoutCreate
from schemas.programs import ProgramCreate
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users")
async def create_user(user: UserUpdate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metric).all()
    # return [
    #     {"title": metric.title, "value": metric.value, "icon": metric.icon}
    #     for metric in metrics
    # ]
    return {"totalUsers": 100, "activePrograms": 50, "monthlyRevenue": 5000, "feedbackCount": 10}

@router.get("/progress")
async def get_progress(db: Session = Depends(get_db)):
    progress = db.query(Progress).all()
    return {
        "labels": [p.week for p in progress],
        "datasets": [
            {
                "label": "Weight Lost",
                "data": [p.weight_lost for p in progress],
                "borderColor": "#FF6B35",
                "tension": 0.4
            },
            {
                "label": "Calories Burned",
                "data": [p.calories_burned for p in progress],
                "borderColor": "#4CAF50",
                "tension": 0.4
            }
        ]
    }
# Program Management
@router.post("/programs")
async def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    print(program)
    new_program = Program(**program.dict())
    db.add(new_program)
    db.commit()
    return new_program

@router.get("/programs")
async def get_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    print("program api called")
    rlist =  [
        {
            "title": program.title,
            "description": program.description,
            "progress": program.progress,
            "duration": program.duration,
            "calories_burned": program.calories_burned,
            "id": program.id
        }
        for program in programs
    ]
    print(rlist)
    return rlist
@router.post("/chat")
async def handle_chatbot_query(query: dict):
    user_message = query.get("message", "").lower()
    
    if "workout" in user_message:
        response = "Try our 30-minute HIIT program today!"
    elif "diet" in user_message:
        response = "Consider a high-protein meal plan with a 500-calorie deficit."
    else:
        response = "How can I assist you with your fitness goals?"
    
    return {"response": response}


# Workout Management
@router.post("/workouts")
async def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    new_workout = Workout(**workout.dict())
    db.add(new_workout)
    db.commit()
    return new_workout

@router.get("/analytics/signups")
async def get_signup_analytics(db: Session = Depends(get_db)):
    # Implementation for signup trends
    return {"labels": ["Jan", "Feb", "Mar"], "data": [150, 200, 180]}

# Trainer Management
@router.post("/trainers")
async def create_trainer(trainer: TrainerCreate, db: Session = Depends(get_db)):
    new_trainer = Trainer(**trainer.dict())
    db.add(new_trainer)
    db.commit()
    return new_trainer

@router.get("/trainers")
async def get_trainers(db: Session = Depends(get_db)):
    trainers = db.query(Trainer).all()
    return [
        {
            "name": trainer.name,
            "specialty": trainer.specialty,
            "experience": trainer.experience
        }
        for trainer in trainers
    ]
# Feedback Management
@router.get("/feedback")
async def get_feedback(resolved: bool = None, db: Session = Depends(get_db)):
    query = db.query(Feedback)
    if resolved is not None:
        query = query.filter(Feedback.resolved == resolved)
    return query.all()