import unittest
from cosmosdb.models.CosmosClient import CosmosClientDatabase
from flask_injector import Injector, singleton
from cosmosdb.services import SERVICES, UserService


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
        user_service: UserService = self.injector.get(UserService)
        self.assertIsNotNone(user_service)

        username1 = 'Carlos'
        password1 = '123'

        username2 = 'Miguel'
        password2 = '321'

        username3 = 'Pinto'
        password3 = '1998'

        username4 = 'Miguel'
        password4 = '2019'

        # Before creating
        self.assertIsNone(user_service.get_user(username1))
        self.assertIsNone(user_service.get_user(username2))

        # Creating two users
        user_doc1 = user_service.add_update(username1, password1)
        user_doc2 = user_service.add_update(username2, password2)

        # Creating an existent user
        user_doc3 = user_service.add_update(username2, password2)

        # After creating
        self.assertIsNotNone(user_service.get_user(username1))
        self.assertIsNotNone(user_service.get_user(username2))

        # User with username3 was not created
        self.assertIsNone(user_service.get_user(username3))

        self.assertEqual(user_doc1['type'], 'User')
        self.assertEqual(user_doc1['username'], username1)
        self.assertEqual(user_doc1['password'], password1)

        self.assertEqual(user_doc2['type'], 'User')
        self.assertEqual(user_doc2['username'], username2)
        self.assertEqual(user_doc2['password'], password2)

        # The third add_update added an existent user
        self.assertIsNone(user_doc3)

        user_doc1_update1 = user_service.add_update(username3, password3, user_doc1['id'])

        # Assert if user info was updated
        self.assertEqual(user_doc1_update1['type'], 'User')
        self.assertEqual(user_doc1_update1['username'], username3)
        self.assertEqual(user_doc1_update1['password'], password3)

        # Won't be updated because there is a user with username4 already in the system
        user_doc1_update2 = user_service.add_update(username4, password4, user_doc1_update1['id'])

        self.assertIsNone(user_doc1_update2)

        # Should use exceptions
        # self.assertRaises(Exception,user_service.add_update, username4, password4, user_doc1_update1['id'])

        # Deleted user_doc1_update1
        user_service.delete_user(user_doc1_update1['id'])

        # Check if the user was deleted
        self.assertIsNone(user_service.get_user_by_id(user_doc1_update1['id']))

        # Trying to delete a not existent user
        # Try to use exceptions to assert this method
        user_service.delete_user(user_doc1_update1['id'])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DBTest)
    unittest.TextTestRunner().run(suite)
