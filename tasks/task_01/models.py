from pydantic import BaseModel
from typing import Optional

class CreateTask(BaseModel):
    name: str
    date: str
    status: Optional[bool] = False

class UpdateTask(BaseModel):
    id: str
    name: Optional[str]
    date: Optional[str]
    status: Optional[bool]

class ToggleTask(BaseModel):
    id: str
    status: bool

class TaskResponse(BaseModel):
    id: str
    name: str
    status: bool
    date: str