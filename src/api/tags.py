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


    op.create_table(
        "user_tag_upvotes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("tag_id", sa.Integer, sa.ForeignKey("user_tags.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("account_users.id")),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

@router.post("/{tag_id}/upvote", response_model=UpvoteResponse, status_code=status.HTTP_202_ACCEPTED)
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
        
