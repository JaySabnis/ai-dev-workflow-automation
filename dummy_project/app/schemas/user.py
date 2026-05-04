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


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    scores: list[int]
    average_score: Optional[float]


class ScoreResponse(BaseModel):
    id: int
    user_id: int
    score: int
