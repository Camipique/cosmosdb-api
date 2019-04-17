from flask_injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase


class UserService:
    @inject
    def __init__(self, db: CosmosClientDatabase):
        self.client_db = db

    def get_users(self):
        query = "SELECT * FROM c"
        users = self.client_db.client.QueryItems(self.client_db.containers_id['User'], query)

        result = [{'username': user['username'], 'password': user['password']}for user in users]

        return result

    def get_user_by_username(self, username):

        query = {
            "query": "SELECT * FROM u WHERE u.username=@username",
            "parameters": [{"name": "@username",
                            "value": username}
                           ]
        }

        result = self.client_db.client.QueryItems(self.client_db.containers_id['User'], query)
        user = next(iter(result))

        return {'username': user['username'], 'password': user['password']}

    def add_user(self, username, password):

        user = {
            'username': username,
            'password': password
        }

        # TODO check if already exists or use pk (?)
        self.client_db.client.CreateItem(self.client_db.containers_id['User'], user)
