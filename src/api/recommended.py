from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List

router = APIRouter(
    prefix="/recommended",
    tags=["recommended"],
    dependencies=[Depends(auth.get_api_key)],
)


class Recommended(BaseModel):
    user_id: int


@router.post("", response_model=List[Recommended])
def recommend(user_id: int):
    """
    Recomends users that have made a tag with the same song or same tag title.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT DISTINCT other.user_id
                FROM user_tags AS my
                JOIN user_tags AS other 
                ON my.track_id = other.track_id OR my.tag_text = other.tag_text
                WHERE my.user_id = :target_user_id
                AND other.user_id != :target_user_id;
                """
            ),
            {"target_user_id": user_id},
        )
    return [Recommended(user_id=row.user_id) for row in result]
