import os
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

db_uri = os.environ.get('DB_URI')
engine = sa.create_engine(db_uri)
metadata = sa.MetaData(bind=engine)

datatable = sa.Table('data', metadata,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('date_loaded', sa.DateTime),
                     sa.Column('load_name', sa.Text),
                     sa.Column('data', JSONB, nullable=False)
                     )
