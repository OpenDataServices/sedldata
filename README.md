# SEDL data

Social Economy Data Lab data wrangling

This is probably just where the script(s) for loading data from a spreadsheet or something will go.

## Setup

At the moment you need to put the postgres database URI in an environment variable on the host.

```
export DB_URI=postgresql://user:pa55w0rd@localhost/database
```

TODO: configure this better

## Do stuff

* `sedldata upgrade`: alembic creates the database
* `sedldata load infile.xlsx outfile.json`: unflattens the input and dumps it to the database
* `sedldata dump`: dumps the rows

## Flattentool

Flattentool command to unflatten sample data.

```
flatten-tool unflatten -f xlsx -o unflattened.json -m deals --metatab-name Meta --metatab-vertical-orientation 'outfile.xlsx' --id-name identifier
```

