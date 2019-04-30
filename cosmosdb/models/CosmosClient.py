from azure.cosmos import cosmos_client
from azure.cosmos.errors import HTTPFailure


class CosmosClientDatabase:

    def __init__(self, args):

        self.client = cosmos_client.CosmosClient(
            url_connection=args['endpoint'],
            auth={'masterKey': args['primary_key']}
        )

        self.create_db_if_not_exists(args['database_name'])
        self.database_id = 'dbs/' + args['database_name']

        self.create_containers_if_not_exists(self.database_id, args['containers'])
        self.containers_id = [self.database_id + '/colls/' + container_name for container_name in args['containers']]

    def create_db_if_not_exists(self, db_name):
        try:
            self.client.ReadDatabase('dbs/'+db_name)
        except HTTPFailure:
            self.client.CreateDatabase({'id': db_name})

    def create_containers_if_not_exists(self, database_id, containers):
        for container_id in containers:
            container_link = database_id+'/colls/'+container_id
            try:
                self.client.ReadContainer(container_link)
            except HTTPFailure:
                self.client.CreateContainer(database_id, {'id': container_id})

    def delete_db(self):
        try:
            self.client.DeleteDatabase(self.database_id)
        except HTTPFailure:
            print("Something wrong in delete_db().")

    def get_container(self, container_name):
        try:
            return self.client.ReadContainer(container_name)
        except HTTPFailure:
            return None

    def get_containers(self):
        return self.containers_id

