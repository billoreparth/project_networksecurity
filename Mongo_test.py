
from pymongo.mongo_client import MongoClient

url = "mongodb+srv://pbuser1:angooduser@clusterp.nqhma.mongodb.net/?retryWrites=true&w=majority&appName=Clusterp"

# Create a new client and connect to the server
client = MongoClient(url)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)