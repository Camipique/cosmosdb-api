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
        return [store for store in stores]

    def get_store(self, store_name):
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
        return next(iter(result), None)

    def get_store_by_id(self, _id):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.id=@id",
            "parameters": [
                {
                    "name": "@type",
                    "value": store_type
                },
                {
                    "name": "@id",
                    "value": _id
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        return next(iter(result), None)

    def add_update(self, store_name, items=None, _id=None):
        store_doc = None
        # add new store
        if not _id:
            if not self.get_store(store_name):
                store = {
                    'type': store_type,
                    'store_name': store_name,
                    'items': items
                }

                # TODO each item should be updated since they will be in this store

                store_doc = self.client_db.client.CreateItem(self.client_db.get_container_id('StoreObject'), store)
        else:
            store_doc = self.get_store_by_id(_id)
            store_doc_by_store_name = self.get_store(store_name)

            if store_doc and (not store_doc_by_store_name or store_doc_by_store_name['id'] == _id):
                store_doc['store_name'] = store_name
                # TODO add items
                self.client_db.client.ReplaceItem(store_doc['_self'], store_doc)
            else:
                store_doc = None

        return store_doc

    def delete_store(self, _id):

        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.id=@id",
            "parameters": [
                {
                    "name": "@type",
                    "value": store_type
                },
                {
                    "name": "@id",
                    "value": _id
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        store = next(iter(result), None)

        if store:
            self.client_db.client.DeleteItem(store['_self'])
