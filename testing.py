from pymongo import MongoClient
from bson.objectid import ObjectId

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://gryffindor:5KpAocBl5RDmr9XrXM6ZVWhhP0R14rXxKaL5jBQKVGrxqC4Sr1iNELIrh0xXcuBTSpVZLR9TOUs5ACDbS7FuDA%3D%3D@gryffindor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@gryffindor@')
# client = MongoClient('mongodb://gryffindor:5KpAocBl5RDmr9XrXM6ZVWhhP0R14rXxKaL5jBQKVGrxqC4Sr1iNELIrh0xXcuBTSpVZLR9TOUs5ACDbS7FuDA%3D%3D@gryffindor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@gryffindor@')
db = client.get_database("sssv1")
collection = db.get_collection("restauents_comments")
user = db.get_collection("users")
myquery = { "name": "tatva" }
myquery2 = {"userid":3}
id ="63ac6dd1ed41cbb87b5ab4f8"
# collection.find_one(ObjectId(id))
cursor = user.find_one(myquery2)

print(cursor)
# for x in cursor:
#   print(x)