"""Add plant

Revision ID: 5c06f243b0bd
Revises: 
Create Date: 2021-11-18 13:11:46.097053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c06f243b0bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plant', sa.Column('last_watered', sa.DateTime(), nullable=True))
    op.add_column('plant', sa.Column('moisture_level', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('plant', 'moisture_level')
    op.drop_column('plant', 'last_watered')
    # ### end Alembic commands ###
