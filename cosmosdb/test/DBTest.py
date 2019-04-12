import unittest
from azure.cosmos import cosmos_client


class DBTest(unittest.TestCase):

    config = {
        'ENDPOINT': 'https://localhost:8081',
        'PRIMARYKEY': 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==',
        'DATABASE': 'CosmosDatabase',
        'CONTAINERS': [
            'User',
            'Item'
        ]
    }

    def setUp(self):
        # Initialize cosmos client, we can also define connection_policy and consistency_level
        self.client = cosmos_client.CosmosClient(
            url_connection=DBTest.config['ENDPOINT'],
            auth={'masterKey': DBTest.config['PRIMARYKEY']}
        )

        self.db = self.client.CreateDatabase({'id': DBTest.config['DATABASE']})

        options = {
            'offerThroughput': 400
        }

        self.containers = {}

        for container in DBTest.config['CONTAINERS']:
            self.containers[container] = self.client.CreateContainer(self.db['_self'], {'id': container}, options)

    def tearDown(self):
        self.client.DeleteDatabase(self.db['_self'])
        # pass

    def testDB(self):
        self.assertIsNotNone(self.db)

    def testContainers(self):
        item_container = self.containers['Item']
        self.assertIsNotNone(item_container)

        user_container = self.containers['User']
        self.assertIsNotNone(user_container)

    def testAddItem(self):
        
        name = "car"
        price = 3500

        car = self.client.CreateItem(
            self.containers['Item']['_self'],
            {
                'name': name,
                'price': price
                # 'store': store_id
            }
        )

        self.assertIsNotNone(car)

        query = {'query': "SELECT * FROM item i"}

        options = {
            'enableCrossPartitionQuery': True
        }

        result = self.client.QueryItems(self.containers['Item']['_self'], query, options)

        itemIter = iter(result)
        item = next(itemIter)

        self.assertEqual(item['name'], name)
        self.assertEqual(item['price'], price)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DBTest)
    unittest.TextTestRunner().run(suite)
