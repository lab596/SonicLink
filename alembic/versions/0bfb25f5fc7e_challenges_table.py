"""Challenges table

Revision ID: 0bfb25f5fc7e
Revises: 8ea516b7be74
Create Date: 2025-05-10 13:00:02.672478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bfb25f5fc7e'
down_revision: Union[str, None] = '8ea516b7be74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "lyrical_moments",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("track_id", sa.String, sa.ForeignKey("spotify_songs.track_id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("account_users.id")),
        sa.Column("moment_text", sa.String, nullable=False),
        sa.Column("song_timestamp", sa.String, nullable=False),
        sa.Column("song_lyric", sa.String, nullable=True),
        sa.Column(
            "timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
    )
    
    op.create_table(
        "challenges",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("account_users.id")),
        sa.Column(
            "timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
    )
    
    op.create_table(
        "challenge_submissions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("challenge_id", sa.Integer, sa.ForeignKey("challenges.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("account_users.id")),
        sa.Column("tag_submission", sa.Integer, sa.ForeignKey("user_tags.id")),
        sa.Column(
            "timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("lyrical_moments")
    op.drop_table("challenges")
    op.drop_table("challenge_submissions")

