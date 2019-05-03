import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import Flask
from flask_restful import Api
from flask_injector import FlaskInjector, singleton
from flask_cors import CORS
from cosmosdb.models.CosmosClient import CosmosClientDatabase
from cosmosdb.services import SERVICES

app = Flask(__name__)
CORS(app)
api = Api(app=app)


def configure(binder):
    endpoint = 'https://localhost:8081'
    primary_key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
    database_name = 'CosmosDatabase'
    containers = [
        'StoreObject'
    ]

    args = {
        'endpoint': endpoint,
        'primary_key': primary_key,
        'database_name': database_name,
        'containers': containers
    }

    db = CosmosClientDatabase(args)
    binder.bind(CosmosClientDatabase, to=db, scope=singleton)

    for service in SERVICES:
        binder.bind(service, scope=singleton)


injector = FlaskInjector(app=app, modules=[configure])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
