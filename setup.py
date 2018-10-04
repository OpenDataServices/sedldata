from setuptools import setup

setup(
    name='sedldata',
    version='0.0.1',
    license='BSD',
    py_modules=['sedldata'],
    install_requires=[
        'Click',
        'SQLAlchemy',
        'alembic',
        'psycopg2',
        'configparser'
    ],
    entry_points='''
        [console_scripts]
        sedldata=sedldata.cli:cli
    ''',
)