from flask_injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase

user_type = 'User'


class UserDoesNotExist(Exception):
    pass


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
        return [user for user in users]

    def get_user(self, username):
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

        result = self.client_db.client.QueryItems(self.client_db.get_container_id('StoreObject'), query)
        user = next(iter(list(result)), None)

        return user

    def get_user_by_id(self, _id):
        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.id=@id",
            "parameters": [
                {
                    "name": "@type",
                    "value": user_type
                },
                {
                    "name": "@id",
                    "value": _id
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.get_container_id('StoreObject'), query)
        return next(iter(list(result)), None)

    def add_update(self, username, password, _id=None):
        user_doc = None

        if not _id:
            if not self.get_user(username):
                user = {
                    'type': user_type,
                    'username': username,
                    'password': password
                }

                user_doc = self.client_db.client.CreateItem(self.client_db.get_container_id('StoreObject'), user)
        else:
            user_doc = self.get_user_by_id(_id)
            user_doc_by_username = self.get_user(username)

            if not user_doc_by_username or user_doc_by_username['id'] == user_doc['id']:
                user_doc['username'] = username
                user_doc['password'] = password
            else:
                user_doc = None

        return user_doc

    def delete_user(self, _id):

        query = {
            "query": "SELECT * FROM o WHERE o.type=@type AND o.id=@id",
            "parameters": [
                {
                    "name": "@type",
                    "value": user_type
                },
                {
                    "name": "@id",
                    "value": _id
                }
            ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['StoreObject'], query)
        user = next(iter(list(result)), None)

        if user:
            self.client_db.client.DeleteItem(user['_self'])
