"""Init

Revision ID: 09789f11b2fd
Revises: 
Create Date: 2018-08-13 15:13:07.081787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09789f11b2fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('meta',
    				sa.Column('load_datetime', sa.DateTime),
    				sa.Column('data_source', sa.Text)
    	)


def downgrade():
    op.drop_table('meta')
