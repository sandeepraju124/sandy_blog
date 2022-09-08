import pymongo
from flask import Flask, json
from flask import render_template, request, Response
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
# client = pymongo.MongoClient("mongodb://mongodb-flask:BvFOOXd0cOoU9vETxCZsDbaPrwrfcoraV3fTkNoWueaFpD4amKvIsM8Gu42hcviJ2Xfz3qfOShu84hxoVgL5iA==@mongodb-flask.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-flask@")
db = client['SSSv1']
app = Flask(__name__)
# db = client['sandeep']
collection = db.restaurant



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # content = request.get_json(force = True)
        try:
            data = request.form.get("email")
            collection.insert_one({"email": data})
            return "inserted data"
        except Exception as e:
            # print(e)
            return e
    return render_template('index.html')



##########      GET  all the users        #################



@app.route('/users',methods=["GET"])
def users():
    try:
        data = list(collection.find())
        for users in data:
            users["_id"]= str(users["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    
    except:
        return Response(response = json.dumps({"message":"user not created"}),status = 200,mimetype="application/json")
    

##########      Post the users        #################

@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        try:
            name = request.form.get("name")
            looks = request.form.get("looks")
            response = collection.insert_one({"name":name,"looks":looks})
            # response = collection.insert_one(dict)
            print(response.inserted_id)
            return Response(response = json.dumps({"message":"user created", "id": f"{response.inserted_id}"}),status = 200,mimetype="application/json")
        except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"user not created"}),status = 500,mimetype="application/json")
        # return jsonify(dict)
    
    
##########      patch the users        #################

@app.route("/users/<id>",methods=["PATCH"])
def usersPatch(id):
    try:
        data = collection.update_one(
        {"_id":ObjectId(id)},
        {"$set":{"name":request.form.get("name")}}
        # {"$set":{"_id":request.form.get("id")}}
        )
        print("xnxnxnxnxnxnxnxnxnxnxnxnxnx")
        print(request.form.get("name"))
        return Response(response=json.dumps({"message":"user updated"}),status = 200,mimetype="application/json")
    except Exception as ex:
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKK{}".format(ex))
        return Response(response=json.dumps({"message":"sry cannot update user"}),status = 500,mimetype="application/json")

# db.products.updateOne({_id: 1}, {$set: {price: 899}})

if __name__ == '__main__':
    app.run(debug=True)
