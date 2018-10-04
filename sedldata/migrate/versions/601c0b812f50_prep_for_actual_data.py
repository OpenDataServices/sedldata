"""Prep for actual data

Revision ID: 601c0b812f50
Revises: 09789f11b2fd
Create Date: 2018-08-20 19:25:35.836266

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '601c0b812f50'
down_revision = '09789f11b2fd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('data',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('date_loaded', sa.DateTime),
                    sa.Column('data', JSONB, nullable=False),
                    )
    op.drop_table('meta')


def downgrade():
    op.create_table('meta',
                    sa.Column('load_datetime', sa.DateTime),
                    sa.Column('data_source', sa.Text)
                    )
    op.drop_table('data')
