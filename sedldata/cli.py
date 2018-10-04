import os
import click
import datetime

import alembic.config

from sedldata.database import datatable
from sedldata.lib import upgrade as lib_upgrade
from sedldata.lib import load as lib_load


@click.group()
def cli():
    pass


@cli.command()
def upgrade():
    lib_upgrade()


@cli.command()
@click.argument('infile')
@click.argument('outfile')
@click.option('--name', default=None)
def load(infile, outfile, name):
    lib_load(infile, outfile, name)


@cli.command()
def dump():
    # Dump the datatable
    click.echo("Dump\n")

    select = datatable.select()
    rows = select.execute()
    for row in rows:
        print(row)
