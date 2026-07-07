from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["rentradar_db"]

# Collection
properties_collection = db["properties"]