from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    age: int


class AddScoreRequest(BaseModel):
    score: int


class UpdateScoreRequest(BaseModel):
    score: int


class CreatedUserResponse(BaseModel):
    id: int
    name: str
    age: int
    created_at: datetime
    updated_at: datetime


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    scores: list[int]
    average_score: Optional[float]
    created_at: datetime
    updated_at: datetime


class ScoreResponse(BaseModel):
    id: int
    user_id: int
    score: int
    created_at: datetime
    updated_at: datetime
