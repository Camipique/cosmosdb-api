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
from cosmosdb.services import SERVICES, UserService, ItemService, StoreService

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

user_service = UserService(injector.injector.get(CosmosClientDatabase, scope=singleton))
item_service = ItemService(injector.injector.get(CosmosClientDatabase, scope=singleton))
store_service = StoreService(injector.injector.get(CosmosClientDatabase, scope=singleton))

user_service.add_user('Carlos', 'password')
user_service.add_user('Miguel', 'drowssap')
user_service.add_user('Pinto', 'password123')
print(user_service.get_users())
user_service.delete_user('Carlos')
print(user_service.get_users())

print('----------------')

store_service.add_store('store1')
store_service.add_store('store2')
print(store_service.get_stores())
store_service.delete_store('store2')
print(store_service.get_stores())

print('----------------')

item_service.add_item('Carlos', 3500, 'store1')
item_service.add_item('Carlos', 3500, 'store1')
print(item_service.get_items())

print('----------------')

print(store_service.get_stores())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
