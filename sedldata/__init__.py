import getpass

from sedldata.database import db
from sedldata.lib import delete_collection
from sedldata.lib import load, load_xlsx, in_notebook, run_sql, get_results, generate_migration


if in_notebook():
    db_uri = 'postgresql://sedldata:{}@46.43.2.250:5432/sedldata'.format(getpass.getpass("Enter database password:  "))
    db.init_db(db_uri)
    db.upgrade()
else:
    db.init_db()


