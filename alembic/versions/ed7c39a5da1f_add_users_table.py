"""Add users table

Revision ID: ed7c39a5da1f
Revises:
Create Date: 2025-04-30 15:23:50.293997

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed7c39a5da1f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "account_users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column(
            "timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("account_users")
