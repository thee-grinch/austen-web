from pydantic import BaseModel
from typing import List, Optional

class TrainerBase(BaseModel):
    name: str
    specialization: str
    contact: str

class TrainerCreate(TrainerBase):
    pass

class TrainerUpdate(TrainerBase):
    pass