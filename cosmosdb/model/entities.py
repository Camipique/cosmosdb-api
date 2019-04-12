from azure.cosmos import cosmos_client


class Database:
    def __init__(self, config, container_options):

        self.client = cosmos_client.CosmosClient(
            url_connection=config['ENDPOINT'],
            auth={'masterKey': config['PRIMARYKEY']}
        )

        self.db = self.client.CreateDatabase({'id': config['DATABASE']})

        self.containers = {}

        for container in config['CONTAINERS']:
            self.containers[container] = self.client.CreateContainer(self.db['_self'], {'id': container}, container_options)
