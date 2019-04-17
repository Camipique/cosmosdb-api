import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

from flask import Flask
from flask_restful import Api
from flask_injector import FlaskInjector, singleton, inject
from flask_cors import CORS

from cosmosdb.models.CosmosClient import CosmosClientDatabase
from cosmosdb.services import SERVICES, UserService

app = Flask(__name__)
CORS(app)
api = Api(app=app)


def configure(binder):
    endpoint = 'https://localhost:8081'
    primary_key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
    database_name = 'CosmosDatabase'
    containers = [
        'User',
        'Item',
        'Store'
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

user_service = UserService(injector.injector.get(CosmosClientDatabase, scope=singleton))

# print(user_service.get_users())
# user_service.add_user('Carlos', 'password')
# user_service.add_user('Miguel', 'drowssap')
# user_service.add_user('Pinto', 'password123')
# print(user_service.get_users())
# print(user_service.get_user_by_username('Carlos'))
# print(user_service.get_user_by_username('Miguel'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
