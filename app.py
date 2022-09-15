import pymongo
from flask import Flask, json
from flask import render_template, request, Response
from bson.objectid import ObjectId

# client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
client = pymongo.MongoClient("mongodb://sandydb:7WV8hpWGNL9EtSzXhk38dZ4tE4wa40ShLkrqKiDqZzhBOqloIrNvFji5UzJ9UgIQSpou5mPyzoy0QOWQYgvQmQ==@sandydb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@sandydb@")
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
            restaurant_name = request.form.get("restaurant_name")
            dp_image = request.form.get("dp_image")
            cover_image = request.form.get("cover_image")
            contact_number = request.form.get("contact_number")
            comments=request.form.getlist("comments")
            rating = request.form.get("rating")
            nreviews = request.form.get("nreviews")
            address = request.form.get("address")
            print(comments)
            response = collection.insert_one({"restaurant_name":restaurant_name,"dp_image":dp_image,"cover_image":cover_image,"contact_number":contact_number,"comments":comments,"rating":rating,"nreviews":nreviews,"address":address})
            print(response.inserted_id)
            return Response(response = json.dumps({"message":"data send", "id": f"{response.inserted_id}"}),status = 200,mimetype="application/json")
        except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"data not send"}),status = 500,mimetype="application/json")
        # return jsonify(dict)
    
    
##########      patch the users        #################

@app.route("/users/<id>",methods=["PATCH"])
def usersPatch(id):
    try:
        data = collection.update_one(
        {"_id":ObjectId(id)},
        # {"$set":{"name":request.form.get("name")}}
        {"$push":{"comments":request.form.get("comments")}}
        )
        print("xnxnxnxnxnxnxnxnxnxnxnxnxnx")
        print(request.form.get("comments"))
        return Response(response=json.dumps({"message":"user updated"}),status = 200,mimetype="application/json")
    except Exception as ex:
        print("KKKKKKKKKKKKKKKKKKKKKKKKKKK{}".format(ex))
        return Response(response=json.dumps({"message":"sry cannot update user"}),status = 500,mimetype="application/json")

# db.products.updateOne({_id: 1}, {$set: {price: 899}})



if __name__ == '__main__':
    app.run(debug=True)
