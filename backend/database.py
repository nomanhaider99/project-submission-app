from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("MONGO_URI")

def connect_to_database():
    client = MongoClient(DATABASE_URI, server_api=ServerApi('1'))
    db = client["database"]
    try:
        client.admin.command('ping')
        print("🔥 You successfully connected to MongoDB!")
        return db
    except Exception as e:
        print(e)
        return
