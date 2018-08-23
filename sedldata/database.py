import os
import sqlalchemy as sa
from configparser import ConfigParser
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


def db_uri():
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


db_uri = db_uri()
engine = sa.create_engine(db_uri)
metadata = sa.MetaData(bind=engine)

datatable = sa.Table('data', metadata,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('date_loaded', sa.DateTime),
                     sa.Column('load_name', sa.Text),
                     sa.Column('data', JSONB, nullable=False)
                     )
