import os
import json
import click
import datetime
import alembic.config
import sqlalchemy as sa

from sedldata.database import datatable


def xl_to_json(infile):
    json_data = """
{
    "deals": [
        {
            "id": "123",
            "org": "Acme Ltd.",
            "value": "1,000,000",
            "investments": [
                {
                    "id": "abc",
                    "description": "Sketchy stuff"
                },
                {
                    "id": "efg",
                    "description": "Definitely not explosives"
                }
            ]
        }
    ]
}
"""
    try:
        with open(os.path.join(infile)) as file:
            # TODO: unflatten
            data = json.loads(json_data)
    except Exception as e:
        raise e
    
    return data


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
@click.argument('infile')
def load(infile):
    # Load something into the database
    now = datetime.datetime.now()
    unflattened = xl_to_json(infile)
    i = datatable.insert()
    i.execute(date_loaded=now, data=unflattened)
    click.echo("Loaded at: %s" % now)


@cli.command()
def dump():
    # Dump the datatable
    click.echo("Dump\n")

    s = datatable.select()
    rows = s.execute()
    for row in rows:
        print(row)