from json import dumps
import pymongo
from flask import Flask, json
from flask import render_template, request, Response
from bson.objectid import ObjectId

# client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
client = pymongo.MongoClient("mongodb://dataisland:MH5bV8Uu4sSCadrPTaZEGiZEp8zscaRLSVEaOybT25ZkDMrCGyWStB5OMp4vzotSGQ2v3Lg49piFACDb6by78g==@dataisland.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@dataisland@")
db = client['sssv1']
app = Flask(__name__)
# db = client['sandeep']
# collection = db.restaurant
collection = db.restauents_comments
user_collection = db.users
services_collection = db.services




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

# @app.route("/users/<id>",methods=["PATCH"])
# def usersPatch(id):
#     try:
#         data = collection.update_one(
#         {"_id":ObjectId(id)},
#         # {"$set":{"name":request.form.get("name")}}
#         {"$push":{"comments":request.form.get("comments")}}
#         )
#         print("xnxnxnxnxnxnxnxnxnxnxnxnxnx")
#         print(request.form.get("comments"))
#         return Response(response=json.dumps({"message":"user updated"}),status = 200,mimetype="application/json")
#     except Exception as ex:
#         print("KKKKKKKKKKKKKKKKKKKKKKKKKKK{}".format(ex))
#         return Response(response=json.dumps({"message":"sry cannot update user"}),status = 500,mimetype="application/json")

# db.products.updateOne({_id: 1}, {$set: {price: 899}})

####################################################################
##########      GET all restaurent comments        #################
####################################################################

@app.route("/rescomments",methods=["GET"])
def rescomments():
    data = list(collection.find())
    # print(data)
    for users in data:
        users["_id"]= str(users["_id"])
    return Response(response = json.dumps(data),status = 200,mimetype="application/json")

##########      GET only 1 restaurent by providing ID        #################

@app.route("/rescommentid/<id>",methods=["GET"])
def rescommentid(id):
    data = collection.find_one(ObjectId(id))
    # print(data)
    # for users in data:
    data["_id"]= str(data["_id"])
    return Response(response = json.dumps(data),status = 200,mimetype="application/json")


##########      GET only 1 restaurent by providing restaurent name        #################

@app.route("/rescommentname/<resname>",methods=["GET"])
def rescommentname(resname):
    data = collection.find_one({ "name": resname})
    # print(data)
    # for users in data:
    data["_id"]= str(data["_id"])
    return Response(response = json.dumps(data),status = 200,mimetype="application/json")

####################################################################
##########      GET all user data        #################
####################################################################

@app.route("/user",methods=["GET","POST"])
def user():
    if request.method=='GET':
        print("hitted get in user")
        data = list(user_collection.find())
        # print(data)
        for users in data:
            users["_id"]= str(users["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    elif request.method=='POST':
        print("hitted post in user")
        name = request.form['name']
        username = request.form['username']
        email = request.form["email"]
        dp = request.form["dp"]
        street = request.form['street']
        state = request.form['state']
        zipcode = request.form['zipcode']
        lat = request.form['lat']
        lng = request.form['lng']
        userid = request.form['userid']
        result = user_collection.insert_one({
                'name':name, 
                'username':username,
                'email':email,
                'dp':dp,
                "zipcode":zipcode,
                "address":{
                    "street":street,
                    "state":state,
                    "geo": {
                            "lat":lat,
                            "lng":lng
                            }
                },
                "userid":userid
                })
        return dumps({'id': str(result.inserted_id)})


##########      GET only 1 user by providing username        #################

# @app.route("/user/<username>",methods=["GET"])
# def singleuser(username):
#     data = user_collection.find_one({ "username": username})
#     print(data)
#     # for users in data:
#     data["_id"]= str(data["_id"])
#     return Response(response = json.dumps(data),status = 200,mimetype="application/json")

##########      GET only 1 user by providing user id        #################

@app.route("/user/<userid>",methods=["GET"])
def singleuserid(userid):
    try:
        data = user_collection.find_one({ "userid":userid})
        
        # for users in data:
        data["_id"]= str(data["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"data not send"}),status = 500,mimetype="application/json")


################ post user comment ######################

@app.route("/postcomment",methods=["POST"])
def postcomment():
    comment = request.form['comment']
    user_id= request.form['user_id']
    resname= request.form['resname']
    # result = collection.update(
    #     {'name': resname}, 
    #     {"$set": {
    #     "comments": {
    #         "comment":comment,
    #         "userid":userid}
    #     }}
    #     )

    new_comment = {
        "comment": comment,
        "first_name": "John",
        "id": 123,
        "last_name": "Doe",
        "user_id": user_id
    }

    result = collection.update_one(
        {"name": resname},
        {"$push": {"comments": new_comment}}
    )
    return "done"


####################################################################
##################      services        #################
####################################################################

################ get all services ######################
@app.route('/services',methods=["GET"])
def services():
    try:
        data = list(services_collection.find())
        for users in data:
            users["_id"]= str(users["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    
    except:
        return Response(response = json.dumps({"message":"no data available"}),status = 500,mimetype="application/json")

################ get services by catogory ######################
@app.route("/services/<service>",methods=["GET"])
def services_selected(service):
    try:
        data = list(services_collection.find({"catagory": service}))
        # print("this is data {}".format(data)) 
        for users in data:
            users["_id"]= str(users["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")

################ get services by id ######################
@app.route("/serviceid/<id>",methods=["GET"])
def services_selected_Id(id):
    try:
        print("this is id {}".format(id))
        data = services_collection.find_one(ObjectId(id))
        print("this is data {}".format(data)) 
        # for users in data:
        #     users["_id"]= str(users["_id"])
        data["_id"]= str(data["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True)
