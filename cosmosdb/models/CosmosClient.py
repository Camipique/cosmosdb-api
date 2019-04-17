from azure.cosmos import cosmos_client
from azure.cosmos.errors import HTTPFailure


class CosmosClientDatabase:

    def __init__(self, args):

        self.client = cosmos_client.CosmosClient(
            url_connection=args['endpoint'],
            auth={'masterKey': args['primary_key']}
        )

        create_db_if_not_exists(self.client, args['database_name'])

        self.database_id = 'dbs/' + args['database_name']

        create_containers_if_not_exists(self.client, self.database_id, args['containers'])

        self.containers_id = {container_name: self.database_id + '/colls/' + container_name for container_name in args['containers']}


def create_db_if_not_exists(client, db_name):
    try:
        client.ReadDatabase('dbs/'+db_name)
    except HTTPFailure:
        client.CreateDatabase({'id': db_name})


def create_containers_if_not_exists(client, database_id, containers):
    for container_id in containers:
        container_link = database_id+'/colls/'+container_id
        try:
            client.ReadContainer(container_link)
        except HTTPFailure:
            client.CreateContainer(database_id, {'id': container_id})
