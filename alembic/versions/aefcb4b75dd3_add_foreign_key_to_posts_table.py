"""add foreign-key to posts table

Revision ID: aefcb4b75dd3
Revises: f7cfd9b32633
Create Date: 2023-01-05 20:40:37.928771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aefcb4b75dd3'
down_revision = 'f7cfd9b32633'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',local_cols=['owner_id'], 
    remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column('posts', 'owner_id')
