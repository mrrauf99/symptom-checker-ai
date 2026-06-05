from pymongo import MongoClient

from backend.config.settings import (
    MONGODB_URI,
    DATABASE_NAME
)

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

predictions_collection = db["predictions"]