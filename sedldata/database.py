import os
import sqlalchemy as sa

db_uri = os.environ.get('DB_URI')
engine = sa.create_engine(db_uri)
metadata = sa.MetaData(bind=engine)

metatable = sa.Table('meta', metadata,
                     sa.Column('load_datetime', sa.DateTime),
                     sa.Column('data_source', sa.Text)
                     )
