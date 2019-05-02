from flask_injector import inject
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

    def add_update(self, name, price, store=None, _id=None):
        item_doc = None

        if not _id:
            items = self.get_items(name)
            for item in items:
                if item['name'] == name and not item['store']:  # Trying to add same item
                    return None
                elif item['name'] == name and store == item['store']:  # Trying to add the same item in the same store
                    return None

            item = {
                'type': item_type,
                'name': name,
                'price': price,
                'store': store
            }

            # TODO add item to the store, if store is specified

            item_doc = self.client_db.client.CreateItem(self.client_db.get_container_id('StoreObject'), item)
        else:
            pass

        return item_doc

        # if not self.get_item_by_name(name, store):
        #         #     query = {
        #         #         "query": "SELECT * FROM o WHERE o.type=@type AND o.store_name=@store_name",
        #         #         "parameters": [
        #         #             {
        #         #                 "name": "@type",
        #         #                 "value": store_type
        #         #             },
        #         #             {
        #         #                 "name": "@store_name",
        #         #                 "value": store
        #         #             }
        #         #         ]
        #         #     }
        #         #
        #         #     result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        #         #
        #         #     store = result.fetch_next_block()[0]
        #         #
        #         #     if store['items']:
        #         #         store['items'] = store['items'].append(item)
        #         #     else:
        #         #         store['items'] = [item]
        #         #
        #         #     self.client_db.client.ReplaceItem(store['_self'], store)
        #         #     self.client_db.client.CreateItem(self.client_db.containers_id['StoreObject'], item)

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
