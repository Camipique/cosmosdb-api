from injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase

item_type = "Item"


class ItemService:
    @inject
    def __init__(self, db: CosmosClientDatabase):
        self.client_db = db

    def get_all_items(self):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type",
            "parameters": [
                {
                    "name": "@type",
                    "value": item_type
                }
            ]
        }

        items = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        return [item for item in items]

    # Return all items with given name, since it is possible to have items with same names in different stores
    def get_items(self, name):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.name=@name",
            "parameters": [
                {
                    "name": "@type",
                    "value": item_type
                },
                {
                    "name": "@name",
                    "value": name
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        return iter(result)

    def get_store_item(self, name, store):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.name=@name AND o.store=@store",
            "parameters": [
                {
                    "name": "@type",
                    "value": item_type
                },
                {
                    "name": "@name",
                    "value": name
                },
                {
                    "name": "@store",
                    "value": store
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        return next(iter(result), None)

    def get_item_by_id(self, _id):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.id=@id",
            "parameters": [
                {
                    "name": "@type",
                    "value": item_type
                },
                {
                    "name": "@id",
                    "value": _id
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        return next(iter(result), None)

    def add_update(self, name, price, store=None, _id=None):

        if self.get_store_item(name, store):  # item already exists in the store
            return None

        if not _id:
            item = {
                'type': item_type,
                'name': name,
                'price': price,
                'store': store
            }

            # TODO add item to the store, if store is specified

            item_doc = self.client_db.client.CreateItem(self.client_db.get_container_id('StoreObject'), item)
        elif not store:  # update an item that is not associated with a store
            item_doc = self.get_item_by_id(_id)

            if not item_doc:
                return None

            item_doc['name'] = name
            item_doc['price'] = price
            self.client_db.client.ReplaceItem(item_doc['_self'], item_doc)
        else:  # _id and store specified
            item_doc = self.get_item_by_id(_id)

            if not item_doc:
                return None

            item_doc['name'] = name
            item_doc['price'] = price
            item_doc['store'] = store

            # TODO add item to the store
            self.client_db.client.ReplaceItem(item_doc['_self'], item_doc)

        return item_doc

    def delete_item(self, _id):

        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.id=@id",
            "parameters": [
                {
                    "name": "@type",
                    "value": item_type
                },
                {
                    "name": "@id",
                    "value": _id
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        item = next(iter(result))

        if item:
            # TODO delete item from store, if it is in one
            self.client_db.client.DeleteItem(item['_self'])
