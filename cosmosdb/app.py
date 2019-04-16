from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from azure.cosmos import cosmos_client

app = Flask(__name__)
CORS(app)
api = Api(app=app)


# if db exists, returns it, else creates
def create_db_if_not_exists(clt, db_name):
    databases = list(clt.ReadDatabases())

    for database in databases:
        if database['id'] == db_name:
            return database

    return client.CreateDatabase({'id': db_name})


def create_container_in_db_if_not_exists(clt, db_link, containers_to_add):
    containers = list(clt.ReadContainer())

    for container in containers_to_add:
        if container == db_name:
            return database

    return client.CreateDatabase({'id': db_name})


endpoint = 'https://localhost:8081'
primary_key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
database_name = 'CosmosDatabase'
containers = [
    'User',
    'Item'
]

container_options = {
    'offerThroughput': 400
}

client = cosmos_client.CosmosClient(
            url_connection=endpoint,
            auth={'masterKey': primary_key}
        )
db = create_db_if_not_exists(client, database_name)
db_link = db['_self']

create_container_in_db_if_not_exists



# for container in containers:
#    container_links[container] = client.CreateContainer(db['_self'], {'id': container}, container_options)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
