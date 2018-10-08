import os

from configparser import ConfigParser
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


def create_db_uri():
    db_uri = os.environ.get('DB_URI')
    if db_uri is None:
        db_params = config()
        db_uri = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            db_params['user'],
            db_params['password'],
            db_params['host'],
            db_params['port'],
            db_params['database'])

    return db_uri


engine = None
metadata = None

deal_table = None
org_table = None
organization_table = None

def init_db(db_uri=None):
    global deal_table
    global org_table
    global engine
    global metadata
    if engine:
        return

    if not db_uri:
        db_uri = create_db_uri()
    engine = sa.create_engine(db_uri)
    metadata = sa.MetaData(bind=engine)

    deal_table = sa.Table('deal', metadata,
                          sa.Column('id', sa.Integer, primary_key=True),
                          sa.Column('collection', sa.Text, nullable=False),
                          sa.Column('deal_id', sa.Text, nullable=False),
                          sa.Column('date_loaded', sa.DateTime),
                          sa.Column('deal', JSONB, nullable=False),
                          sa.Column('metadata', JSONB)
                         )

    org_table = sa.Table('organization', metadata,
                          sa.Column('id', sa.Integer, primary_key=True),
                          sa.Column('collection', sa.Text, nullable=False),
                          sa.Column('org_id', sa.Text, nullable=False),
                          sa.Column('date_loaded', sa.DateTime),
                          sa.Column('organization', JSONB, nullable=False),
                          sa.Column('metadata', JSONB)
                        )
