
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List
import Levenshtein

router = APIRouter(
    prefix="/recommended",
    tags=["recommended"],
    dependencies=[Depends(auth.get_api_key)],
)


class Recommended(BaseModel):
    user_id: int
    similarity_score: float

    
@router.get("/{user_id}", response_model=List[Recommended])
def recommend(user_id: int):
    """
    Recommends users that have made a tag with the same song or same tag title.
    """
    
    with db.engine.begin() as connection:
       #fetches tags the user has created
        user_tags = connection.execute(
            sqlalchemy.text("""
                SELECT tag_text, track_id
                FROM user_tags
                WHERE user_id = :uid
            """), {"uid": user_id}
        ).fetchall()
        
        #get the tags of other users
        other_tags = connection.execute(
            sqlalchemy.text("""
                SELECT user_id, tag_text, track_id
                FROM user_tags
                WHERE user_id != :uid
            """), {"uid": user_id}
        ).fetchall()
    
    #using an ai model to judge tag similiarity
    user_tag_texts = [tag.tag_text for tag in user_tags]
    if not user_tag_texts:
        return []
        
    #fetch other user tags
    other_user_tags = defaultdict(list)
    for row in other_tags:
        other_user_tags[row.user_id].append(row.tag_text)
    
    #calculate similarity
    recommendations = []
    for other_uid, tag_list in other_user_tags.items():
        total_similarity = 0
        comparison = 0

        for user_tag in user_tag_texts:
            for other_tag in tag_list:
                similarity = Levenshtein.ratio(user_tag, other_tag)
                total_similarity += similarity
                comparison += 1
        
        if comparison > 0:
            avg_similarity = total_similarity / comparison
            if avg_similarity >= 0.6:  #arbitrary threshold
                recommendations.append(
                    Recommended(user_id=other_uid, similarity_score=round(avg_similarity, 3))
                )
        
    #sort similiarity
    recommendations.sort(key=lambda r: r.similarity_score, reverse=True)
    return recommendations
