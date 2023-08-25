"""add content column to posts table

Revision ID: bd27fb9583a4
Revises: abbac9f0eda7
Create Date: 2023-08-25 11:29:54.217905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd27fb9583a4"
down_revision: Union[str, None] = "abbac9f0eda7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
