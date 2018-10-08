import os
from configparser import ConfigParser

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


class Database:

    def __init__(self, engine=None, metadata=None, deal_table=None, org_table=None):
        self.engine = engine
        self.metadata = metadata
        self.deal_table = deal_table
        self.org_table = org_table

    def config(self, filename='database.ini', section='postgresql'):
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

    def create_db_uri(self):
        db_uri = os.environ.get('DB_URI')
        if db_uri is None:
            db_params = self.config()
            db_uri = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
                db_params['user'],
                db_params['password'],
                db_params['host'],
                db_params['port'],
                db_params['database'])

        return db_uri

    def init_db(self, db_uri=None):
        if self.engine:
            return

        if not db_uri:
            db_uri = self.create_db_uri()
        self.engine = sa.create_engine(db_uri)
        self.metadata = sa.MetaData(bind=self.engine)

        self.deal_table = sa.Table(
            'deal', self.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('collection', sa.Text, nullable=False),
            sa.Column('deal_id', sa.Text, nullable=False),
            sa.Column('date_loaded', sa.DateTime),
            sa.Column('deal', JSONB, nullable=False),
            sa.Column('metadata', JSONB)
        )

        self.org_table = sa.Table(
            'organization', self.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('collection', sa.Text, nullable=False),
            sa.Column('org_id', sa.Text, nullable=False),
            sa.Column('date_loaded', sa.DateTime),
            sa.Column('organization', JSONB, nullable=False),
            sa.Column('metadata', JSONB)
        )
