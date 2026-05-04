from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user import (
    CreateUserRequest, AddScoreRequest, UpdateScoreRequest,
    CreatedUserResponse, UserResponse, ScoreResponse,
)
import service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    try:
        data = service.get_user_data(str(user_id), db)
        return {**data, "id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@router.post("", response_model=CreatedUserResponse, status_code=201)
def create_user(body: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        return service.create_user(body.name, body.age, db)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/{user_id}/scores", response_model=ScoreResponse, status_code=201)
def add_score(user_id: int, body: AddScoreRequest, db: Session = Depends(get_db)):
    try:
        return service.add_score_for_user(user_id, body.score, db)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")


@router.put("/{user_id}/scores/{score_id}", response_model=ScoreResponse)
def update_score(user_id: int, score_id: int, body: UpdateScoreRequest, db: Session = Depends(get_db)):
    try:
        return service.update_score_for_user(user_id, score_id, body.score, db)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")
