"""Import Spotify Database

Revision ID: 8ea516b7be74
Revises: ed7c39a5da1f
Create Date: 2025-05-04 10:33:54.453920

"""
import csv
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import kagglehub
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision: str = '8ea516b7be74'
down_revision: Union[str, None] = 'ed7c39a5da1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


spotify_songs = table(
    "spotify_songs",
    column("track_id", sa.String),
    column("artists", sa.String),
    column("album_name", sa.String),
    column("track_name", sa.String),
    column("duration", sa.Integer),
)


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "spotify_songs",
        sa.Column("track_id", sa.String, primary_key=True),
        sa.Column("artists", sa.String, nullable=True),
        sa.Column("album_name", sa.String, nullable=True),
        sa.Column("track_name", sa.String, nullable=True),
        sa.Column("duration", sa.Integer, nullable=True),
    )
    
    dataset_dir = Path(
        kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")
    )
    
    csv_path = dataset_dir / "dataset.csv"
    
    batch, seen_ids = [], set()
    with csv_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            track_id = row["track_id"]
            if track_id in seen_ids:
                continue

            seen_ids.add(track_id)
            batch.append(
                {
                    "track_id": track_id,
                    "artists": row["artists"],
                    "album_name": row.get("album_name"),
                    "track_name": row.get("track_name"),
                    "duration": int(row.get("duration_ms", 0)) // 1000,
                }
            )
            if len(batch) == 10000:
                op.bulk_insert(spotify_songs, batch)
                batch.clear()
                break
    
    if batch:
        op.bulk_insert(spotify_songs, batch)
        
    op.create_table(
        "user_tags",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("track_id", sa.String, sa.ForeignKey("spotify_songs.track_id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("account_users.id")),
        sa.Column("tag_text", sa.String, nullable=False),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    
    op.create_table(
        "user_tag_upvotes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("tag_id", sa.Integer, sa.ForeignKey("user_tags.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("account_users.id")),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("spotify_songs")
    op.drop_table("user_tags")
    op.drop_table("user_tag_upvotes")
