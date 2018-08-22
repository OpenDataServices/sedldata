"""identifier for data load

Revision ID: 954def4c1b92
Revises: 601c0b812f50
Create Date: 2018-08-22 13:56:11.419775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954def4c1b92'
down_revision = '601c0b812f50'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('data', sa.Column('load_name', sa.Text))


def downgrade():
    op.drop_column('data', 'load_name')
