from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from cosmosdb.model.entities import Database

app = Flask(__name__)
CORS(app)
api = Api(app=app)

endpoint = 'https://localhost:8081'
primary_key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
database_name = 'CosmosDatabase'
containers = [
    'User',
    'Item'
]

config = {
        'ENDPOINT': endpoint,
        'PRIMARYKEY': primary_key,
        'DATABASE': database_name,
        'CONTAINERS': containers
    }

container_options = {
    'offerThroughput': 400
}

db = Database(config, container_options)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
