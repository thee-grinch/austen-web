from pydantic import BaseModel

class userCreate(BaseModel):
    username: str
    email: str
    password: str

class userLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str
    email: str
    is_active: bool

class WorkoutCreate(BaseModel):
    name: str
    description: str
    duration: int
    calories: float

class TrainerCreate(BaseModel):
    name: str
    specialization: str
    contact: str

