import os
import json
import click
import datetime

import alembic.config
import sqlalchemy as sa
from flattentool import unflatten

from sedldata.database import datatable


def xl_to_json(infile, outfile):
    try:
        unflatten(
                input_name=infile,
                output_name=outfile,
                input_format='xlsx',
                metatab_name='Meta',
                metatab_vertical_orientation=True,
                root_list_path='deals',
                id_name='id',
                root_id='')
        with open(outfile,'r') as json_file:
            data = json.load(json_file)
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

    alembic_cfg_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'alembic.ini'))
    alembicargs = [
        '--config', alembic_cfg_path,
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicargs)


@cli.command()
@click.argument('infile')
@click.argument('outfile')
@click.option('--name', default=None)
def load(infile, outfile, name):
    if name is None:
        name = infile
    # Load something into the database
    now = datetime.datetime.now()
    unflattened = xl_to_json(infile, outfile)
    insert = datatable.insert()
    insert.execute(date_loaded=now, load_name=name, data=unflattened)
    click.echo("Loaded %s at: %s" % (name, now))


@cli.command()
def dump():
    # Dump the datatable
    click.echo("Dump\n")

    select = datatable.select()
    rows = select.execute()
    for row in rows:
        print(row)
