# Stores API using CosmosDB
This is an API built with Flask and Flask-RESTful for a simple online store.
 
Instead of using Pony ORM to manage and access the database, it uses Azure Cosmos DB.


## Requirements
- Python3, install [here](https://www.python.org/downloads/)
- Virtual environments

## Setup
Install requirements
```
virtualenv --python=python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Install using windows cmd
```
virtualenv --python=python3 .venv
cd .venv/Scripts
activate
cd ..
cd ..
pip install -r requirements.txt
```

## Run
Make sure you are in the virtual environment and, in the stores folder, run
```
python app.py
```

