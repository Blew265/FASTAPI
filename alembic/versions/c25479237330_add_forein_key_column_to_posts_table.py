"""add forein-key column to posts table

Revision ID: c25479237330
Revises: 851054e493f6
Create Date: 2024-04-28 12:03:08.727971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c25479237330'
down_revision: Union[str, None] = '851054e493f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",  local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
 
def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
