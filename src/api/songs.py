from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    dependencies=[Depends(auth.get_api_key)],
)
class SongRequest(BaseModel):
    search: str

class SongResponse(BaseModel):
    song_title: str
    song_id: str

@router.get("/{search}", response_model=List[SongResponse])
def get_songs(search: str):
    """
    Retrieve all songs that match search
    """

    with db.engine.begin() as connection:
        # returns songs that match search, limit to 50 for readability of results
        row = connection.execute(
            sqlalchemy.text(
                """ 
                SELECT
                    track_name,
                    track_id
                FROM spotify_songs
                WHERE track_name ILIKE :search
                LIMIT 50
                """
            ),
            {"search": f"%{search}%"},
        ).fetchall()

    return [
        SongResponse(
            song_title= r.track_name,
            song_id=r.track_id,
        )
        for r in row
    ]
