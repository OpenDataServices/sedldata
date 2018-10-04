import os
import getpass
import subprocess

from sedldata.lib import upgrade, load, load_xlsx, in_notebook, run_sql, get_results
from sedldata.database import init_db


if in_notebook():
    db_uri = 'postgresql://sedldata:{}@46.43.2.250:5432/sedldata'.format(getpass.getpass("Enter database password:  "))
    init_db(db_uri)
    upgrade()
else:
    init_db()


