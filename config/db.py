
from pymongo import MongoClient

var_url = f"mongodb+srv://joeysabusido:genesis11@cluster0.bmdqy.mongodb.net/ldglobal?retryWrites=true&w=majority"

client = MongoClient(var_url)

mydb = client['ldglobal']

collection = mydb.login

async def fetch_user():
    """This is to fetch all user"""
    document =  collection.find()
    return document