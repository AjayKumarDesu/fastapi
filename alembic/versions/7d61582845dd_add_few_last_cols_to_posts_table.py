"""add few last cols to posts table

Revision ID: 7d61582845dd
Revises: aefcb4b75dd3
Create Date: 2023-01-05 20:52:34.560981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d61582845dd'
down_revision = 'aefcb4b75dd3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))



def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
