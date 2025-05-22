from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List


router = APIRouter(
    prefix="/lyrical-moments",
    tags=["lyrical-moments"],
    dependencies=[Depends(auth.get_api_key)],
)


class MomentCreateRequest(BaseModel):
    user_id: int
    song_id: str
    timestamp_seconds: int
    lyric: str
    moment_text: str

class LyricalMomentResponse(BaseModel):
    user_id: int
    moment_text: str
    song_timestamp: str     # change to int later
    # song_lyric: str


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_moment(req: MomentCreateRequest):
    """
    Create a new lyrical moment for a song.
    """
    with db.engine.begin() as connection:
        # make sure the user exists
        user_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM account_users WHERE id = :uid"),
            {"uid": req.user_id},
        ).fetchone()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")

        # make sure we have a valid song timestamp
        song_duration = connection.execute(
            sqlalchemy.text(
                "SELECT duration FROM spotify_songs WHERE track_id = :songid"
            ),
            {"songid": req.song_id},
        ).first()

        # print(song_duration[0])
        if not song_duration or not song_duration[0]:
            raise HTTPException(status_code=404, detail="Song not found")
        elif req.timestamp_seconds > song_duration[0] or req.timestamp_seconds < 0:
            raise HTTPException(status_code=400, detail="Invalid song duration")

        result = connection.execute(
            sqlalchemy.text("""
                INSERT INTO lyrical_moments (track_id, user_id, moment_text, song_timestamp, song_lyric)
                VALUES (:track_id, :user_id, :moment_text, :song_timestamp, :song_lyric)
                RETURNING id
            """),
            {
                "track_id": req.song_id,
                "user_id": req.user_id,
                "moment_text": req.moment_text,
                "song_timestamp": req.timestamp_seconds,
                "song_lyric": req.lyric,
            },
        ).one()

    return {"moment_id": result[0], "message": "Lyrical Moment created successfully"}

@router.get("/{song_id}", response_model=List[LyricalMomentResponse])
def get_all_moments(song_id: str):
    """
    Returns all lyrical moments of a song
    """
    with db.engine.begin() as connection:
        # make sure the user exists
        song_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM spotify_songs WHERE track_id = :sid"),
            {"sid": song_id},
        ).fetchone()
        if not song_exists:
            raise HTTPException(status_code=404, detail="Song not found")
        
        song_moments = []
        
        # Query all lyrical moments of the song
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT 
                    user_id, 
                    moment_text,
                    song_timestamp
                FROM lyrical_moments
                WHERE track_id = :sid
                """
            ),
            {"sid": song_id}
        ).fetchall()

        for row in rows:
            song_moments.append(
                LyricalMomentResponse(
                    user_id=row.user_id,
                    moment_text=row.moment_text,
                    song_timestamp=row.song_timestamp
                )
            )

    print(f"Lyrical moments for track_id {song_id}")
    return song_moments
