"""add content column to posts table

Revision ID: 20683da06108
Revises: beb985301c82
Create Date: 2023-01-05 17:44:56.243569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20683da06108'
down_revision = 'beb985301c82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
