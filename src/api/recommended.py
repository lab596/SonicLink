
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List
from sentence_transformers import SentenceTransformer, util


router = APIRouter(
    prefix="/recommended",
    tags=["recommended"],
    dependencies=[Depends(auth.get_api_key)],
)
model = SentenceTransformer('all-MiniLM-L6-v2')


class Recommended(BaseModel):
    user_id: int
    similarity_score: float

    
@router.get("/{user_id}", response_model=List[Recommended])
def recommend(user_id: int):
    """
    Recomends users that have made a tag with the same song or same tag title.
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
    
    user_embeddings = model.encode(user_tag_texts, convert_to_tensor=True)
    
    #fetch other user tags
    other_user_tags = defaultdict(list)
    for row in other_tags:
        other_user_tags[row.user_id].append(row.tag_text)
    
    #compare ai model results
    recommendations = []
    for other_uid, tag_list in other_user_tags.items():
        other_embeddings = model.encode(tag_list, convert_to_tensor=True)

        #fancy math idk really know what it does
        cosine_scores = util.cos_sim(user_embeddings, other_embeddings)

        #get similiarity
        max_similarities = cosine_scores.max(dim=1).values
        avg_similarity = float(max_similarities.mean())
        
        print(avg_similarity)

        if avg_similarity >= 0.6:  #arbitrary threshold
            recommendations.append(
                Recommended(user_id=other_uid, similarity_score=round(avg_similarity, 3))
            )

    #sort similiarity
    recommendations.sort(key=lambda r: r.similarity_score, reverse=True)
    return recommendations
