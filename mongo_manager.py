from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class MongoManager:
    MONGOURI = os.getenv("MONGOURI")

    def __init__(self, db_name):
        self.db_name = db_name
        self.client = MongoClient(self.MONGOURI)
        self.db = self.client[db_name]

    def find_one(self, collection, query):

        data = self.db[collection].find_one(query)
        return data

    def insert_one(self, collection, data):
        id = self.db[collection].insert_one(data).inserted_id
        if id:
            return True
        return False
