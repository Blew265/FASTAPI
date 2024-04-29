"""add content column to posts table

Revision ID: f0053799c059
Revises: b7a81e87216c
Create Date: 2024-04-28 11:23:34.033171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0053799c059'
down_revision: Union[str, None] = 'b7a81e87216c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
