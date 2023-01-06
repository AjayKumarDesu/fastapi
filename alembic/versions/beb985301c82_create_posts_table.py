"""create posts table

Revision ID: beb985301c82
Revises: 
Create Date: 2023-01-05 17:22:57.934073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beb985301c82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
    sa.Column('id', sa.Integer(), nullable= False, primary_key = True), 
    sa.Column('title', sa.String(), nullable= False))
    


def downgrade() -> None:
    op.drop_table('posts')
    
