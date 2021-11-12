""" 
Ryan Kite
CSD 310
Nov 10, 2021
Module 5
Assignment 5.2
Description: 
Collection Creation
"""

""" import statements """
from pymongo import MongoClient

# connection uri
url = "mongodb+srv://admin:admin@kite.jjgxi.mongodb.net/pytech?retryWrites=true&w=majority"

# connect to mongo
client = MongoClient(url)

# connect pytech database
db = client.pytech

# display collections 
print("\n Pytech \n")

print("List collection names: ", db.list_collection_names())
print("\n")
print(dir(db))


