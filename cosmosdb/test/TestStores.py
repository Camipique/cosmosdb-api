import unittest
from cosmosdb.models.CosmosClient import CosmosClientDatabase
from flask_injector import Injector, singleton
from cosmosdb.services import SERVICES, StoreService, ItemService


class DBTest(unittest.TestCase):

    def setUp(self):

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

        self.injector = Injector(modules=[configure])
        self.db = self.injector.get(CosmosClientDatabase)

    def tearDown(self):
        self.db.delete_db()

    def test_db_exists(self):
        self.assertIsNotNone(self.db)

    def test_container_exists(self):
        for container_id in self.db.get_containers():
            self.assertIsNotNone(self.db.get_container(container_id))

        self.assertIsNone(self.db.get_container('NotContainer'))

    def test_stores(self):
        store_service: StoreService = self.injector.get(StoreService)
        self.assertIsNotNone(store_service)

        store1 = 'store1'
        store2 = 'store2'
        store3 = 'store3'
        store4 = 'store2'

        # Before creating stores
        self.assertIsNone(store_service.get_store(store1))
        self.assertIsNone(store_service.get_store(store2))

        # Add new store
        store_doc1 = store_service.add_update(store_name=store1)
        store_doc2 = store_service.add_update(store_name=store2)

        # Add existent store
        store_doc3 = store_service.add_update(store_name=store2)

        self.assertIsNotNone(store_doc1)
        self.assertIsNotNone(store_doc2)

        self.assertIsNone(store_doc3)

        self.assertEqual(store_doc1['type'], 'Store')
        self.assertEqual(store_doc1['store_name'], store1)
        self.assertIsNone(store_doc1['items'])

        self.assertEqual(store_doc2['type'], 'Store')
        self.assertEqual(store_doc2['store_name'], store2)
        self.assertIsNone(store_doc2['items'])

        # Update store_doc1 name
        store_doc1_update1_store_name = store_service.add_update(store_name=store3, _id=store_doc1['id'])

        self.assertEqual(store_doc1_update1_store_name['type'], 'Store')
        self.assertEqual(store_doc1_update1_store_name['store_name'], store3)
        self.assertIsNone(store_doc1_update1_store_name['items'])

        # store name that was subbed
        self.assertIsNone(store_service.get_store(store1))

        # Update store_doc1 name to an existing one
        store_doc1_update2_store_name = store_service.add_update(store_name=store4, _id=store_doc1_update1_store_name['id'])

        self.assertIsNone(store_doc1_update2_store_name)

        # Delete store
        store_service.delete_store(store_doc1_update1_store_name['id'])

        # Check if the store was deleted
        self.assertIsNone(store_service.get_store(store_doc1_update1_store_name['store_name']))

    def test_items(self):
        item_service: ItemService = self.injector.get(ItemService)
        self.assertIsNotNone(item_service)

        item1 = 'item1'
        price1 = 10.0

        item2 = 'item2'
        price2 = 20.0

        item3 = 'item3'
        price3 = 30.0

        item4 = 'item2'
        price4 = 40.0

        # Add new store
        item_doc1 = item_service.add_update(item1, price1)
        item_doc2 = item_service.add_update(item2, price2)

        # Add existent store
        item_doc3 = item_service.add_update(item2, price2)

        self.assertIsNotNone(item_doc1)
        self.assertIsNotNone(item_doc2)

        self.assertIsNone(item_doc3)

        self.assertEqual(item_doc1['type'], 'Item')
        self.assertEqual(item_doc1['name'], item1)
        self.assertEqual(item_doc1['price'], price1)
        self.assertIsNone(item_doc1['store'])

        self.assertEqual(item_doc2['type'], 'Item')
        self.assertEqual(item_doc2['name'], item2)
        self.assertEqual(item_doc2['price'], price2)
        self.assertIsNone(item_doc2['store'])

        # # Update store_doc1 name
        # store_doc1_update1_store_name = store_service.add_update(store_name=store3, _id=store_doc1['id'])
        #
        # self.assertEqual(store_doc1_update1_store_name['type'], 'Store')
        # self.assertEqual(store_doc1_update1_store_name['store_name'], store3)
        # self.assertIsNone(store_doc1_update1_store_name['items'])
        #
        # # store name that was subbed
        # self.assertIsNone(store_service.get_store(store1))
        #
        # # Update store_doc1 name to an existing one
        # store_doc1_update2_store_name = store_service.add_update(store_name=store4, _id=store_doc1_update1_store_name['id'])
        #
        # self.assertIsNone(store_doc1_update2_store_name)
        #
        # # Delete store
        # store_service.delete_store(store_doc1_update1_store_name['id'])
        #
        # # Check if the store was deleted
        # self.assertIsNone(store_service.get_store(store_doc1_update1_store_name['store_name']))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DBTest)
    unittest.TextTestRunner().run(suite)
