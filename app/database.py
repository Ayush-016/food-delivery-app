from pymongo import MongoClient
from app.config import MONGO_URL


client = MongoClient(MONGO_URL)

db = client["food_delivery"]

users_collection = db["users"]
food_collection = db["foods"]
order_collection = db["orders"]