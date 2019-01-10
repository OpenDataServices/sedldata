import os
from configparser import ConfigParser

import alembic.config
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


#special global just to give db to alembic
db = None

class Database:

    def __init__(self, db_uri=None):
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

    def upgrade(self):
        # only alembic commands should update the global db
        global db
        db = self

        # Let alembic create the tables
        alembic_cfg_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'alembic.ini'))
        alembicargs = [
            '--config', alembic_cfg_path,
            '--raiseerr',
            'upgrade', 'head',
        ]
        alembic.config.main(argv=alembicargs)

    def generate_migration(self, name):
        # only alembic commands should update the global db
        global db
        db = self
        print("Generating database migrations")

        alembic_cfg_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'alembic.ini'))
        alembicargs = [
            '--config', alembic_cfg_path,
            '--raiseerr',
            'revision', '--autogenerate', '-m', name
        ]
        alembic.config.main(argv=alembicargs)


