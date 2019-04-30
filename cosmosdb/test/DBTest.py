import unittest
from cosmosdb.models.CosmosClient import CosmosClientDatabase
from flask_injector import Injector, singleton
from cosmosdb.services import SERVICES


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

    def test_add_user(self):
        pass

    # def testAddItem(self):
    #
    #     name = "car"
    #     price = 3500
    #
    #     car = self.client.CreateItem(
    #         self.containers['Item']['_self'],
    #         {
    #             'name': name,
    #             'price': price
    #             # 'store': store_id
    #         }
    #     )
    #
    #     self.assertIsNotNone(car)
    #
    #     query = {'query': "SELECT * FROM item i"}
    #
    #     options = {
    #         'enableCrossPartitionQuery': True
    #     }
    #
    #     result = self.client.QueryItems(self.containers['Item']['_self'], query, options)
    #
    #     itemIter = iter(result)
    #     item = next(itemIter)
    #
    #     self.assertEqual(item['name'], name)
    #     self.assertEqual(item['price'], price)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DBTest)
    unittest.TextTestRunner().run(suite)
