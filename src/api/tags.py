from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    dependencies=[Depends(auth.get_api_key)],
)

class TagCreateRequest(BaseModel):
    user_id: int
    song_id: str
    tag_text: str

class UpvoteRequest(BaseModel):
    user_id: int
    tag_id: int

class TagResponse(BaseModel):
    tag_id: int
    song_id: str
    tag_text: str
    upvotes: int

class UpvoteResponse(BaseModel):
    message: str

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
                INSERT INTO user_tags (user_id, track_id, tag_text)
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

@router.post("/upvote", response_model=UpvoteResponse, status_code=status.HTTP_202_ACCEPTED)
def create_tag(req: UpvoteRequest):
    """
    Upvote an existing tag with the creator's user id.
    """
    with db.engine.begin() as connection:
        existing_vote = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 FROM user_tag_upvotes
                WHERE tag_id = :tag_id AND user_id = :user_id
                """
            ),
            {"tag_id": req.tag_id, "user_id": req.user_id}
        ).fetchone()
        if existing_vote:
            return UpvoteResponse(message= "User has already upvoted this tag")
    
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO user_tag_upvotes (tag_id, user_id)
                VALUES (:tag_id, :user_id)
                """
            ),
            {"tag_id": req.tag_id, "user_id": req.user_id}
        )
    
    return  UpvoteResponse(message= "Successfully upvoted!")
        
@router.get("/users/{user_id}/tags", response_model=List[TagResponse])
def get_song_tags(user_id: int):
    """
    Retrieve all tags created by a specific user along with upvote counts
    """

    with db.engine.begin() as connection:

        # check if user exists
        user_exists = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1
                FROM account_users
                WHERE id = :uid
                """
            ),
            {"uid": user_id}
        ).one()

        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        # query all tags of the user
        rows = connection.execute(
            sqlalchemy.text(
                """ 
                SELECT
                    ut.id AS tag_id,
                    ut.track_id AS song_id,
                    ut.tag_text,
                    COUNT(utu.user_id) AS upvotes
                FROM user_tags ut
                LEFT JOIN user_tag_upvotes utu ON ut.id = utu.tag_id
                WHERE ut.user_id = :user_id
                GROUP BY ut.id, ut.track_id, ut.tag_text
                ORDER BY ut.timestamp DESC
                """
            ),
            {"user_id": user_id}
        ).fetchall()

    return [
        TagResponse(
            tag_id=row.tag_id,
            song_id=row.song_id,
            tag_text=row.tag_text,
            upvotes=row.upvotes
        )
        for row in rows
    ]