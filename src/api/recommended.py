
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(
    prefix="/recommended",
    tags=["recommended"],
    dependencies=[Depends(auth.get_api_key)],
)


class Recommended(BaseModel):
    user_id: Optional[int] = None
    similarity_score: Optional[float] = None
    message: str

    
@router.get("/{user_id}", response_model=List[Recommended])
def recommend(user_id: int):
    """
    Recommends users that have made a tag with the same song or same tag title.
    """
    
    with db.engine.begin() as connection:
        # make sure user exists
        user_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM account_users WHERE id = :uid"),
            {"uid": user_id},
        ).fetchone()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        all_tags = connection.execute(sqlalchemy.text("""
            SELECT user_id, tag_text
            FROM user_tags
        """)).fetchall()
    
    if not all_tags:
        return [Recommended(
            user_id=None, 
            similarity_score=None,
            message="No tags found"
        )]
    
    #per user document tags
    user_tag_docs = defaultdict(list)
    for row in all_tags:
        user_tag_docs[row.user_id].append(row.tag_text)
    
    if user_id not in user_tag_docs:
        return [Recommended(
            user_id=None, 
            similarity_score=None,
            message="User has no tags"
        )]
    
    user_ids = []
    documents = []
    for uid, tags, in user_tag_docs.items():
        user_ids.append(uid)
        documents.append(" ".join(tags))

    vectorizer = TfidfVectorizer(user_id)
    matrix = vectorizer.fit_transform(documents)

    target_index = user_ids.index(user_id)
    target_vector = matrix[target_index]

    similarity_scores = cosine_similarity(target_vector, matrix).flatten()
    
    #calculate similarity
    recommendations = []
    for idx, avg_similarity in enumerate(similarity_scores):
        if user_ids[idx] == user_id:
            continue
        if avg_similarity >= 0.6:  #arbitrary threshold
            recommendations.append(
                Recommended(
                    user_id=user_ids[idx], 
                    similarity_score=round(float(avg_similarity), 3),
                    message="Recommended user found!"
                )
            )
        
    #sort similiarity
    recommendations.sort(key=lambda r: r.similarity_score, reverse=True)
    return recommendations
