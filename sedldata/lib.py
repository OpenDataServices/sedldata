import json
import os
import datetime
import html

import alembic.config
import jinja2
from flattentool import unflatten



def in_notebook():
    if 'JPY_PARENT_PID' in os.environ:
        return True
    return False


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


def upgrade():
    # Let alembic create the tables
    print("Upgrading database")

    alembic_cfg_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'alembic.ini'))
    alembicargs = [
        '--config', alembic_cfg_path,
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicargs)


def load(infile, outfile, name):
    from sedldata.database import datatable
    if name is None:
        name = infile
    # Load something into the database
    now = datetime.datetime.now()
    unflattened = xl_to_json(infile, outfile)
    insert = datatable.insert()
    insert.execute(date_loaded=now, load_name=name, data=unflattened)
    print("Loaded %s at: %s" % (name, now))


def load_xlsx(collection=None, infile=None, outfile='output.json'):
    if not collection and in_notebook():
        collection = input('Please state collections name: ')
    if not collection:
        raise ValueError('You need to input a non-empty collection name!')

    if in_notebook():
        from google.colab import files
        print('Upload your xlsx SEDL file:')
        uploaded = files.upload()
        for file_name in uploaded:
            infile = 'uploaded.xlsx'
            with open(infile, '+wb') as f:
                f.write(uploaded[file_name])
            break
    
    if not infile:
        raise ValueError('You need to state an input file')

    unflattened = xl_to_json(infile, outfile)

    from sedldata.database import datatable

    now = datetime.datetime.now()
    insert = datatable.insert()
    insert.execute(date_loaded=now, load_name=collection, data=unflattened)
    print("Loaded %s at: %s" % (collection, now))

table = jinja2.Template(
'''
<table>
    <thead>
    <tr>
      {% for header in headers %}
        <th style="text-align: left; vertical-align: top">{{ header }}</th>
      {% endfor %}
    </tr>
    </thead>
    <tbody>
      {% for row in data %}
        <tr>
          {% for cell in row %}
              <td style="text-align: left; vertical-align: top">
                <pre>{{ cell }}</pre>
              </td>
          {% endfor %}
        </tr>
      {% endfor %}
    </tbody>
</table>
'''
)


def generate_rows(result, limit):
    for num, row in enumerate(result):
        if num == limit:
            break
        yield [json.dumps(item, indent=2) if isinstance(item, dict) else html.escape(str(item)) for item in row]


def get_results(sql, limit=-1):
    from sedldata.database import engine

    with engine.begin() as connection:
        sql_result = connection.execute(sql)
        if sql_result.returns_rows:
            results = {
                "data": [row for row in generate_rows(sql_result, limit)],
                "headers": sql_result.keys()
            }
            return results
        else:
            return "Success"


def run_sql(sql, limit=100):
    from IPython.core.display import display, HTML
    results = get_results(sql, limit)
    if results == 'Success':
        return results
    display(HTML(table.render(results)))
