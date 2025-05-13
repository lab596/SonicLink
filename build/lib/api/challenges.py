from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"],
    dependencies=[Depends(auth.get_api_key)],
)


class ChallengeResponse(BaseModel):
    user_id: int

class ChallengeCreateRequest(BaseModel):
    user_id: int
    title: str
    description: str
    

@router.post("", status_code=status.HTTP_201_CREATED)
def create_challenge(req: ChallengeCreateRequest):
    """
    Recomends users that have made a tag with the same song or same tag title.
    """
    with db.engine.begin() as connection:
        user_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM account_users WHERE id = :uid"),
            {"uid": req.user_id},
        ).fetchone()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        
        result = connection.execute(
            sqlalchemy.text("""
                INSERT INTO challenges (user_id, description, title)
                VALUES (:user_id, :description, :title)
                RETURNING id
            """),
            {"user_id": req.user_id,  "title": req.title, "description": req.description},
        ).one()
    return {"challenge_id": result[0], "message": "Challenge created successfully"}
