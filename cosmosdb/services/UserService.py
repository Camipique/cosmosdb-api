from flask_injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase

user_type = 'User'


class UserService:
    @inject
    def __init__(self, db: CosmosClientDatabase):
        self.client_db = db

    def get_users(self):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type",
            "parameters": [
                {
                    "name": "@type",
                    "value": user_type
                }
            ]
        }

        users = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)

        result = [{'username': user['username'], 'password': user['password']} for user in users]

        return result

    def get_user_by_username(self, username):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.username=@username",
            "parameters": [
                {
                    "name": "@type",
                    "value": user_type
                },
                {
                    "name": "@username",
                    "value": username
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)

        for user in result:
            if user['username'] == username:
                return {'username': user['username'], 'password': user['password']}

    def add_user(self, username, password):
        user = {
            'type': user_type,
            'username': username,
            'password': password
        }

        if not self.get_user_by_username(username):
            self.client_db.client.CreateItem(self.client_db.containers_id['StoreObject'], user)

    def delete_user(self, username):

        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.username=@username",
            "parameters": [
                {
                    "name": "@type",
                    "value": user_type
                },
                {
                    "name": "@username",
                    "value": username
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        user = next(iter(result))

        if user:
            self.client_db.client.DeleteItem(user['_self'])
