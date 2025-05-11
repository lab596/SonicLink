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
            {"uid": req.user_id},
        ).fetchone()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        #make sure song exists
        song = connection.execute(
            sqlalchemy.text(
                "SELCT 1 FROM spotify_songs WHERE track_id = :songid"
            ),
            {"songid": req.song_id}
        ).first()
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")

        result = connection.execute(
            sqlalchemy.text("""
                INSERT INTO user_tags (user_id, track_id, tag_text)
                VALUES (:user_id, :song_id, :tag_text)
                RETURNING id
            """),
            {"user_id": req.user_id, "song_id": req.song_id, "tag_text": req.tag_text},
        ).one()

    return {"tag_id": result[0], "message": "Tag created successfully"}


@router.post(
    "/upvote", response_model=UpvoteResponse, status_code=status.HTTP_202_ACCEPTED
)
def create_upvote(req: UpvoteRequest):
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
            {"tag_id": req.tag_id, "user_id": req.user_id},
        ).fetchone()
        if existing_vote:
            return UpvoteResponse(message="User has already upvoted this tag")

        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO user_tag_upvotes (tag_id, user_id)
                VALUES (:tag_id, :user_id)
                """
            ),
            {"tag_id": req.tag_id, "user_id": req.user_id},
        )

    return UpvoteResponse(message="Successfully upvoted!")


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
            {"uid": user_id},
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
            {"user_id": user_id},
        ).fetchall()

    return [
        TagResponse(
            tag_id=row.tag_id,
            song_id=row.song_id,
            tag_text=row.tag_text,
            upvotes=row.upvotes,
        )
        for row in rows
    ]


@router.get("/leaderboard", response_model=List[TagResponse])
def get_leaderboard():
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT 
                    user_tags.id,
                    user_tags.track_id,
                    user_tags.tag_text,
                    COUNT(user_tag_upvotes.id) AS upvote_count
                FROM 
                    user_tag_upvotes 
                JOIN 
                    user_tags ON user_tags.id = user_tag_upvotes.tag_id
                WHERE 
                    user_tag_upvotes.timestamp >= NOW() - INTERVAL '7 days'
                GROUP BY 
                    user_tags.tag_text, user_tags.id,  user_tags.track_id
                ORDER BY 
                    upvote_count DESC
                LIMIT 10;
                """
            )
        ).fetchall()
        leaderboard = []

        for r in row:
            tag_response = TagResponse(
                tag_id=r[0], song_id=r[1], tag_text=r[2], upvotes=r[3]
            )

            leaderboard.append(tag_response)

    return leaderboard


class TagSearchResult(BaseModel):
    song_id: str
    title: str
    artist: str
    tag: str
    tag_id: int


@router.get("/search", response_model=List[TagSearchResult])
def search_tags(text: str):
    """
    Search for songs by tag text (case-insensitive, partial match).
    """
    wildcard_text = f"%{text}%"

    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT 
                    ut.track_id AS song_id,
                    s.track_name,
                    s.artists,
                    ut.tag_text AS tag,
                    ut.id AS tag_id
                FROM user_tags ut
                JOIN spotify_songs s ON ut.track_id = s.track_id
                WHERE ut.tag_text ILIKE :search_text
                ORDER BY ut.timestamp DESC
                """
            ),
            {"search_text": wildcard_text},
        ).fetchall()

    return [
        TagSearchResult(
            song_id=row.song_id,
            title=row.track_name,
            artist=row.artists,
            tag=row.tag,
            tag_id=row.tag_id,
        )
        for row in rows
    ]
