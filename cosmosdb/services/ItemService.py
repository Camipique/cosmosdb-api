from flask_injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase
from cosmosdb.services.StoreService import store_type

item_type = "Item"

class ItemService:
    @inject
    def __init__(self, db: CosmosClientDatabase):
        self.client_db = db

    def get_items(self):
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

        result = [{'name': item['name'], 'price': item['price'], 'store': item['store']} for item in items]

        return result

    def get_raw_item(self, name, store):
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

        for item in result:
            if item['name'] == name:
                return item

    def get_item_by_name(self, name, store):
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

        for item in result:
            if item['name'] == name:
                return {'name': item['name'], 'price': item['price'], 'store': item['store']}

    def add_item(self, name, price, store):
        item = {
            'type': item_type,
            'name': name,
            'price': price,
            'store': store
        }

        if not self.get_item_by_name(name, store):
            query = {
                "query": "SELECT * FROM o WHERE o.type=@type AND o.store_name=@store_name",
                "parameters": [
                    {
                        "name": "@type",
                        "value": store_type
                    },
                    {
                        "name": "@store_name",
                        "value": store
                    }
                ]
            }

            result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)

            store = result.fetch_next_block()[0]

            if store['items']:
                store['items'] = store['items'].append(item)
            else:
                store['items'] = [item]

            self.client_db.client.ReplaceItem(store['_self'], store)
            self.client_db.client.CreateItem(self.client_db.containers_id['StoreObject'], item)

    def delete_item(self, name, store):

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
        item = next(iter(result))

        if item:
            self.client_db.client.DeleteItem(item['_self'])
