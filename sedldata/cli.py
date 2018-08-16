import os
import click
import datetime
import alembic.config
import sqlalchemy as sa

from sedldata.database import metatable


@click.group()
def cli():
    pass


@cli.command()
def upgrade():
    # Let alembic create the tables
    click.echo("Upgrading database")

    alembic_cfg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    alembicargs = [
        '--config', alembic_cfg_path,
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicargs)


@cli.command()
def load():
    # Load something into the database
    now = datetime.datetime.now()
    i = metatable.insert()
    i.execute(load_datetime=now, data_source="Test")
    click.echo("Loaded test: %s" % now)


@cli.command()
def test():
    # Dump the metatable
    click.echo("Dump\n")

    s = metatable.select()
    rows = s.execute()
    for row in rows:
        print(row)