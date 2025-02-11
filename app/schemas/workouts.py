from pydantic import BaseModel

class WorkoutCreate(BaseModel):
    name: str
    description: str
    duration: int
    calories: float

class TrainerCreate(BaseModel):
    name: str
    specialization: str
    contact: str
