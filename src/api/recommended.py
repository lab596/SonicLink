
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
import numpy as np

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
    
    targegt_tags = user_tag_docs[user_id]
    other_user_tags = []
    tag_owners = []
    for uid, tags, in user_tag_docs.items():
        if uid == user_id:
            continue
        for tag in tags:
            other_user_tags.append(tag)
            tag_owners.append(uid)
    if not other_user_tags:
        return [Recommended(
            user_id=None, 
            similarity_score=None,
            message="No user tags to compare"
        )]

    #Vectorize tags
    vectorizer = TfidfVectorizer()
    all_tags = targegt_tags + other_user_tags
    matrix = vectorizer.fit_transform(all_tags)

    #Separate matrices
    num_target_tags = len(targegt_tags)
    target_matrix = matrix[:num_target_tags]
    other_matrix = matrix[num_target_tags:]

    similarity_scores = cosine_similarity(other_matrix, target_matrix)
    
    user_scores = defaultdict(list)
    for i, owner_id in enumerate(tag_owners):
        similarity_row = similarity_scores[i]
        best_similarity = np.max(similarity_row)
        if best_similarity >= 0.6:
            user_scores[owner_id].append(best_similarity)

    #recommendatiosn
    recommendations = []
    for uid, scores in user_scores.items():
        avg_score = sum(scores) / len(scores)
        recommendations.append(Recommended(
            user_id=uid, 
            similarity_score=round(avg_score, 3),
            message="Recommended users based on tags"
        ))
        
    #sort similiarity
    recommendations.sort(key=lambda r: r.similarity_score, reverse=True)
    return recommendations
