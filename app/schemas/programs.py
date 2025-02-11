from pydantic import BaseModel

class ProgramBase(BaseModel):
    title: str
    description: str
    duration: int
    calories_burned: float
    

class ProgramCreate(ProgramBase):
    pass

