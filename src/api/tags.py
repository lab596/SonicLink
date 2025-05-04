from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

class TagCreateRequest(BaseModel):
    user_id: int
    song_id: str
    tag_text: str

class UpvoteRequest(BaseModel):
    user_id: int

class TagResponse(BaseModel):
    tag_id: int
    song_id: str
    tag_text: str
    upvotes: int

@router.post("", status_code=status.HTTP_201_CREATED)
def create_tag(req: TagCreateRequest):
    """
    Create a new tag for a song.
    """
    with db.engine.begin() as connection:
        user_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM account_users WHERE id = :uid"),
            {"uid": req.user_id}
        ).fetchone()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")

        result = connection.execute(
            sqlalchemy.text("""
                INSERT INTO song_tags (user_id, song_id, tag_text)
                VALUES (:user_id, :song_id, :tag_text)
                RETURNING id
            """),
            {
                "user_id": req.user_id,
                "song_id": req.song_id,
                "tag_text": req.tag_text
            }
        ).one()
    
    return {"tag_id": result[0], "message": "Tag created successfully"}
