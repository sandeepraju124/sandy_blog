from pymongo import MongoClient
from bson.objectid import ObjectId

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://entreprenuer:R5vnleLp0q2OwDYOJx8IAeVdfLQgJU1MUYd7MVWU4d71napzz3J5hfDfKjvm4AA39l8t2eAwwFrgACDbcT1XtA==@entreprenuer.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@entreprenuer@')
# client = MongoClient('mongodb://gryffindor:5KpAocBl5RDmr9XrXM6ZVWhhP0R14rXxKaL5jBQKVGrxqC4Sr1iNELIrh0xXcuBTSpVZLR9TOUs5ACDbS7FuDA%3D%3D@gryffindor.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@gryffindor@')
db = client.get_database("sssv1")

# select collection name here
collection = db.get_collection("restauents_comments")
user = db.get_collection("users")
services_comments = db.get_collection("services_comments")


# querys
myquery = { "name": "tatva" }
myquery2 = {"userid":"OMFhNqfW73dYJUbTp9UHumI127r2"}
myquery3 = {"catogory": "barber"}
id ="63ac6dd1ed41cbb87b5ab4f8"


# collection.find_one(ObjectId(id))

# cursor = services.find(myquery3)
# cursor = list(services.find({"catagory": "barber"}))
# document = collection.find_one({"serviceid": "iiiiiiiiiiii"})
# print(document) 
# if document is None:
#     print("none")
#     document = {'serviceid': "xxnxnxnxnnxnx", 'comments': []}
#     print(document)
#     document["comments"].append({"comment":"ooooooooooo","user_id":"vvvvvvvvvvvv"})
#     print(document)
#     collection.insert_one(document)
    # collection.update_one({"serviceid": "63f116b0190416d07f3687ec"}, {'$set': document})
# dataa = {}
data = services_comments.find_one({"business_uid": "SWEFOO1659634920974"})
print(data["comments"])
for i in data["comments"]:
    print("this is i")
    print(i["user_id"])
    user_id = i["user_id"]

    cursor = user.find_one({"userid":user_id})
    print(cursor["username"])

print(cursor["dp"])



# cursor = services.find_one(ObjectId('63dfde4110891aa38b95ba0b'))
# print(document)
# print(str(list(cursor)))
# for x in cursor:
#   print(x)