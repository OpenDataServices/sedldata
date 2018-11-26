# SEDL data

Social Economy Data Lab data wrangling

This is probably just where the script(s) for loading data from a spreadsheet or something will go.

## Setup

Postgres database URI can be in an environment variable on the host:

```
export DB_URI=postgresql://user:pa55w0rd@localhost/database
```

Alternatively rename `database.ini.tmpl` to `database.ini` and set params there.

## Do stuff

* `sedldata upgrade`: alembic creates the database
* `sedldata load infile.xlsx outfile.json --name=my_data_load`: unflattens the input and dumps it to the database
  * `--name` is optional and defaults to the input filename if left out. Should be something human-understandable to help you identify a particular data load. Doesn't need to be unique, but probably helpful if it is.
* `sedldata dump`: dumps the rows

## Flattentool

Flattentool command to unflatten sample data.

```
flatten-tool unflatten -f xlsx -o unflattened.json -m deals --metatab-name Meta --metatab-vertical-orientation 'outfile.xlsx'
```

## Servers

* For postgres access and data loading: `ssh root@sedl-db.default.opendataservices.uk0.bigv.io`
  * Copy new data to the server: `scp MY_FILE.xlsx root@sedl-db.default.opendataservices.uk0.bigv.io:/home/sedldata/data/`
* For redash frontend: `http://root@sedl-redash.default.opendataservices.uk0.bigv.io:9090`
