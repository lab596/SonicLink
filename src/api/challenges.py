from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"],
    dependencies=[Depends(auth.get_api_key)],
)


# class ChallengeResponse(BaseModel):
#     user_id: int


class ChallengeCreateRequest(BaseModel):
    user_id: int
    title: str
    description: str


class SubmissionRequest(BaseModel):
    user_id: int
    tag_id: int


class ChallengeLeaderboard(BaseModel):
    challenge_id: int
    title: str
    upvotes: int


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_challenge(req: ChallengeCreateRequest):
    """
    Creates a new challenge with a title and description for users to add their tags
    """
    with db.engine.begin() as connection:
        user_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM account_users WHERE id = :uid"),
            {"uid": req.user_id},
        ).fetchone()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")

        result = connection.execute(
            sqlalchemy.text("""
                INSERT INTO challenges (user_id, description, title)
                VALUES (:user_id, :description, :title)
                RETURNING id
            """),
            {
                "user_id": req.user_id,
                "title": req.title,
                "description": req.description,
            },
        ).one()
    return {"challenge_id": result[0], "message": "Challenge created successfully"}


@router.post("/{challenge_id}/submission", status_code=status.HTTP_204_NO_CONTENT)
def submit_challenge(challenge_id: int, req: SubmissionRequest):
    """
    Sumbit a tag you've made to a challenge
    """
    with db.engine.begin() as connection:
        challenge_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM challenges WHERE id = :challenge_id"),
            {"challenge_id": challenge_id},
        ).fetchone()
        if not challenge_exists:
            raise HTTPException(status_code=404, detail="Challenge not found")

        tag_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM user_tags WHERE id = :tag_id"),
            {"tag_id": req.tag_id},
        ).fetchone()
        if not tag_exists:
            raise HTTPException(status_code=404, detail="Tag not found")

        connection.execute(
            sqlalchemy.text("""
                INSERT INTO challenge_submissions (user_id, challenge_id, tag_submission)
                VALUES (:user_id, :challenge_id, :tag_submission)
            """),
            {
                "user_id": req.user_id,
                "challenge_id": challenge_id,
                "tag_submission": req.tag_id,
            },
        )

    return


@router.post("/weekly", response_model=List[ChallengeLeaderboard])
def weekly_leaderboard():
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    challenges.id AS challenge_id,
                    challenges.title,
                    COUNT(DISTINCT user_tag_upvotes.id) AS total_upvotes
                FROM challenges 
                JOIN challenge_submissions  ON challenges.id = challenge_submissions.challenge_id
                JOIN user_tags ON challenge_submissions.tag_submission = user_tags.id
                LEFT JOIN user_tag_upvotes ON user_tag_upvotes.tag_id = user_tags.id
                WHERE challenges.timestamp >= NOW() - INTERVAL '7 days'
                GROUP BY challenges.id
                ORDER BY total_upvotes DESC
                """
            )
        ).fetchall()
        leaderboard = []

        for r in row:
            tag_response = ChallengeLeaderboard(
                challenge_id=r[0], title=r[1], upvotes=r[2]
            )

            leaderboard.append(tag_response)

    return leaderboard
