import os
import certifi

from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
load_dotenv()

ca = certifi.where()
# uri = "mongodb+srv://sakthi7797:1298504m@cluster1.ojikh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
MONGO_DB_URL = os.getenv("MONGO_DB_URI")

# Create a new client and connect to the server
client = MongoClient(MONGO_DB_URL, tlsCAFile=ca, connectTimeoutMS=30000)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)