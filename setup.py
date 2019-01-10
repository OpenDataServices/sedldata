from setuptools import setup

setup(
    name='sedldata',
    version='0.0.5',
    license='BSD',
    packages=['sedldata', 'sedldata.migrate', 'sedldata.migrate.versions'],
    package_data={'sedldata': ['alembic.ini'], 'sedldata.migrate': 'script.py.mako'},
    install_requires=[
        'Click',
        'SQLAlchemy',
        'alembic',
        'psycopg2-binary',
        'configparser',
        'jinja2',
        'gspread',
        'openpyxl',
        'requests',
        'flattentool'
    ],
    entry_points='''
        [console_scripts]
        sedldata=sedldata.cli:cli
    ''',
)
