# SEDL data

Social Economy Data Lab data wrangling

## Local Setup

For local installation a postgres database needs to be running and you need to link to it using sqlalchemy database URI 
by setting an environment variable DB_URI:

```
export DB_URI=postgresql://user:pa55w0rd@localhost/database
```

Alternatively rename `database.ini.tmpl` to `database.ini` and set params there.

## Do stuff

Look at example usage in notebook:

https://colab.research.google.com/drive/1xdt3N01Qrk2MqQ2qH65BYD6bHzAnO6UX


## Flattentool

Flattentool command to unflatten sample data.

```
flatten-tool unflatten -f xlsx -o unflattened.json -m deals --metatab-name Meta --metatab-vertical-orientation 'outfile.xlsx'
```

## Servers

* For postgres access: `ssh root@sedl-db.default.opendataservices.uk0.bigv.io`
* For redash frontend: `http://root@sedl-redash.default.opendataservices.uk0.bigv.io:9090`
