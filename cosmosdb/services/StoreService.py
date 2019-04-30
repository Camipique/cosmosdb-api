from flask_injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase

store_type = 'Store'


class StoreService:
    @inject
    def __init__(self, db: CosmosClientDatabase):
        self.client_db = db

    def get_stores(self):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type",
            "parameters": [
                {
                    "name": "@type",
                    "value": store_type
                }
            ]
        }

        stores = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)

        result = [{'name': store['store_name'], 'items': store['items']} for store in stores]

        return result

    def get_store_by_name(self, store_name):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.store_name=@store_name",
            "parameters": [
                {
                    "name": "@type",
                    "value": store_type
                },
                {
                    "name": "@store_name",
                    "value": store_name
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)

        store = next(iter(result.fetch_next_block() or []), None)

        if store:
            return [{'store_name': store['store_name'], 'items': store['items']}]

    def add_store(self, store_name):
        store = {
            'type': store_type,
            'store_name': store_name,
            'items': []
        }

        if not self.get_store_by_name(store_name):
            self.client_db.client.CreateItem(self.client_db.containers_id['StoreObject'], store)

    def delete_store(self, store_name):

        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.store_name=@store_name",
            "parameters": [
                {
                    "name": "@type",
                    "value": store_type
                },
                {
                    "name": "@store_name",
                    "value": store_name
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)

        store = next(iter(result.fetch_next_block() or []), None)

        if store:
            return self.client_db.client.DeleteItem(store['_self'])
