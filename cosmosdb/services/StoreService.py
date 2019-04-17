from flask_injector import inject
from cosmosdb.models.CosmosClient import CosmosClientDatabase


class StoreService:
    @inject
    def __init__(self, db: CosmosClientDatabase):
        self.client_db = db
