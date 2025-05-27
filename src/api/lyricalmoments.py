from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src.api import auth
from src import database as db

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


@router.post("", status_code=status.HTTP_201_CREATED)
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

        print(song_duration[0])
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
