import getpass

from sedldata.database import Database
from sedldata.lib import delete_collection
from sedldata.lib import TemporaryClassUpgrade, load, load_xlsx, in_notebook, run_sql, get_results, generate_migration

# db = Database()

if in_notebook():
    db_uri = 'postgresql://sedldata:{}@46.43.2.250:5432/sedldata'.format(getpass.getpass("Enter database password:  "))
    # db.init_db(db_uri)
    # upgrade()
    session = TemporaryClassUpgrade(db_uri=db_uri)
    session.upgrade()
else:
    db = Database()
    db.init_db()


