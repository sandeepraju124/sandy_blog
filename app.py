from json import dumps
import pymongo
from flask import Flask, json, jsonify
from flask import render_template, request, Response
from bson.objectid import ObjectId
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import time
from datetime import datetime

# client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
client = pymongo.MongoClient("mongodb://battle-of-stalingrad:u5Zz811YjnbcJGfgXVxgmRJPtzYop4ZQkHExGH9V823s4XZ8keiaL4DF1BGE9hW5L5xpXrHkql3sACDbl5hj7Q==@battle-of-stalingrad.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@battle-of-stalingrad@")
db = client['sssv1']
app = Flask(__name__)
# db = client['sandeep']
# collection = db.restaurant
service_comments_collection = db.services_comments
user_collection = db.users
services_collection = db.services
askcommunity = db.ask_community



# azure storage details
account_name = 'prometheus1137'
account_key = 'QeCd4oED1ZKVaP0W9ncB7KYUv9qulmESzjb6NCpJQ/OMBlY8eWiSau+Jvu8AMfpV2ce31T6I9Hhy+AStf6oPkg=='
container_name = 'sssv1'
timestamp = int(time.time() * 1000)
print("time")
print(int(time.time()))
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)



# important
# find with object id
# data = list(service_comments_collection.find({"_id": ObjectId(id)}))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # content = request.get_json(force = True)
        try:
            data = request.form.get("email")
            service_comments_collection.insert_one({"email": data})
            return "inserted data"
        except Exception as e:
            # print(e)
            return e
    return render_template('index.html')



##########      GET  all the users        #################



@app.route('/users',methods=["GET"])
def users():
    try:
        data = list(service_comments_collection.find())
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
            response = service_comments_collection.insert_one({"restaurant_name":restaurant_name,"dp_image":dp_image,"cover_image":cover_image,"contact_number":contact_number,"comments":comments,"rating":rating,"nreviews":nreviews,"address":address})
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
    data = list(service_comments_collection.find())
    # print(data)
    for users in data:
        users["_id"]= str(users["_id"])
    return Response(response = json.dumps(data),status = 200,mimetype="application/json")

##########      GET only 1 restaurent by providing ID        #################

@app.route("/serviceIdForComments/<id>",methods=["GET"])
def rescommentIdForComments(id):
    # data = service_comments_collection.find_one(ObjectId(id))
    data = service_comments_collection.find_one({"serviceid": id})
    if data is None:
        return Response(response = json.dumps({"error":"comment not found"}),status=404,mimetype="application/json")
    # print(data)
    # for users in data:
    data["_id"]= str(data["_id"])
    return Response(response = json.dumps(data),status = 200,mimetype="application/json")


##########      GET only 1 restaurent by providing restaurent name        #################

@app.route("/rescommentname/<resname>",methods=["GET"])
def rescommentname(resname):
    data = service_comments_collection.find_one({ "name": resname})
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







####################################################################
##################      services        #################
####################################################################

################ get all services ######################
@app.route('/services',methods=["GET","POST"])
def services():
    if request.method=='GET':
        try:
            data = list(services_collection.find())
            for users in data:
                users["_id"]= str(users["_id"])
            # response_data = {"services": data, "categories": list(categories), "subcategories": list(subcategories)}
            return Response(response = json.dumps(data),status = 200,mimetype="application/json")
        
        
        except:
            return Response(response = json.dumps({"message":"no data available"}),status = 500,mimetype="application/json")
        
    if request.method=='POST':
        try:
            business_name = request.form['business_name']
            business_description = request.form['business_description']
            contact_information = request.form['contact_information']
            country = request.form['country']
            category = request.form['category']
            sub_category = request.form['sub_category']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            profile_image = request.files['profile_image']


            service_fields = {}
            blob_urls = []

            if business_name:
                service_fields["business_name"] = business_name
            if business_description:
                service_fields["business_description"] = business_description
            if contact_information:
                service_fields["contact_information"] = contact_information
            if country:
                service_fields["country"] = country
            if category:
                service_fields["category"] = category
            if sub_category:
                service_fields["sub_category"] = sub_category
            if latitude:
                service_fields["latitude"] = latitude
            if longitude:
                service_fields["longitude"] = longitude

            if 'profile_image' in request.files:
                profile_image = request.files['profile_image']
                filename = profile_image.filename
                print("filename")
                print(filename)
                print(timestamp)
                blob_name = str(timestamp) + '_' + filename
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(profile_image.read())
                blob_url = blob_client.url
                service_fields["profile_image"] = blob_url




            if 'images' in request.files:
                for file in request.files.getlist('images'):
                    filename = file.filename
                    file_extension = filename.split('.')[-1]
                    blob_name = str(timestamp) + '_' + filename
                    blob_client = container_client.get_blob_client(blob_name)

                    blob_client.upload_blob(file.read())
                    blob_urls.append(blob_client.url)

            service_fields["images"] = blob_urls
            # if sub_catagory:
            #     service_fields["images"] = sub_catagory


            services_collection.insert_one(service_fields)
            print("blob_urls {}".format(blob_urls))

            return jsonify({'message': 'Service added successfully.'}), 200
    
        except Exception as e:
            return  jsonify({'message': f'Error adding service: {str(e)}'}), 500



################ get business by category ######################
@app.route("/category/<category>",methods=["GET"])
def category(category):
    try:
        data = list(services_collection.find({"category": category}))
        for users in data:
            users["_id"]= str(users["_id"])
        # categories = set(service['category'] for service in data)
        subcategories = set(service['sub_category'] for service in data)
        response_data = {"services": data,"subcategories": list(subcategories)}
        return Response(response=json.dumps(response_data), status=200, mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")
    
################ get business by subcategory ######################
@app.route("/subcategory/<subcategory>",methods=["GET"])
def subcategory(subcategory):
    try:
        data = list(services_collection.find({"sub_category": subcategory}))
        for users in data:
            users["_id"]= str(users["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")
    

################ get business by uid ######################
@app.route("/uid/<uid>",methods=["GET"])
def uid(uid):
    try:
        data = services_collection.find_one({"business_uid": uid})
        data["_id"]= str(data["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")

################ get business by id ######################

@app.route("/objid/<objid>",methods=["GET"])
def objid(objid):
    try:
        data = services_collection.find_one(ObjectId(objid))
        data["_id"]= str(data["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    except Exception as e:
            print("hitted exemption {}".format(e))
            return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")



# ____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________

########################################################
################ comment section #####################
########################################################

################ get services comments by id ######################

@app.route("/commentsuid/<uid>", methods=["GET"])
def comments_uid(uid):
    try:
        data = service_comments_collection.find_one({"business_uid": uid})
        if data is None:
            # Return an empty comments list if business_uid doesn't match
            data = {"_id": "", "business_uid": uid, "reviews": [],"rating_count": {
                    "5": 0,
                    "4": 0,
                    "3": 0,
                    "2": 0,
                    "1": 0
                },
                "overall_rating": 0 }
        else:
            data["_id"] = str(data["_id"])

            # Loop through the comments and fetch user details from user collection
            for comment in data["reviews"]:
                user_id = comment["user_id"]
                user_data = user_collection.find_one({"userid": user_id})
                comment["username"] = user_data["username"]
                comment["dp"] = user_data["dp"]


                # Calculate the ratings
            rating_count = {
                "5": 0,
                "4": 0,
                "3": 0,
                "2": 0,
                "1": 0
            }
            total_rating = 0

            for comment in data["reviews"]:
                rating = comment.get("rating")
                if rating:
                    total_rating += rating
                    rating_count[str(rating)] += 1

            data["rating_count"] = rating_count
            print("5")
            data["overall_rating"] = round(total_rating / len(data["reviews"]), 1) if len(data["reviews"]) > 0 else 0

        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Error fetching comments"}), status=500, mimetype="application/json")
    

################ post user comment ######################

@app.route("/postcomment", methods=["POST"])
def postcomment():
    try:
        rating = int(request.form['rating'])
        review = request.form['review']
        user_id = request.form['user_id']
        business_uid = request.form['business_uid']

        new_comment = {
            "rating":rating,
            "comment": review,
            "user_id": user_id,
            "created_at": datetime.now().isoformat()  # Use the current timestamp for created_at
        }

        # Check if business_uid exists in the collection
        existing_business = service_comments_collection.find_one({"business_uid": business_uid})

        if existing_business:
            # Update the reviews list in the existing business document
            result = service_comments_collection.update_one(
                {"business_uid": business_uid},
                {"$push": {"reviews": new_comment}}
            )
        else:
            # Create a new collection and insert the document
            new_business = {
                "business_uid": business_uid,
                "reviews": [new_comment]
            }
            result = service_comments_collection.insert_one(new_business)

        return "done"

    except Exception as e:
        return str(e), 500  # Return the error message with a 500 status code




########################################### BACKEND APP #####################################



########################################### testing #####################################

@app.route('/uploadimage',methods=['POST'])
def upload_image():
    try:
        
        file = request.files['image']
        # business_name = request.form['business_name']
        account_name = 'prometheus1137'
        account_key = 'QeCd4oED1ZKVaP0W9ncB7KYUv9qulmESzjb6NCpJQ/OMBlY8eWiSau+Jvu8AMfpV2ce31T6I9Hhy+AStf6oPkg=='
        container_name = 'sssv1'
        timestamp = time.time()
        timestamp_ms = int(timestamp * 1000)
        filename = file.filename
        file_extension = filename.split('.')[-1]
        blob_name = str(timestamp_ms) + '.' + file_extension
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        # DefaultEndpointsProtocol=https;AccountName=prometheus1137;AccountKey=QeCd4oED1ZKVaP0W9ncB7KYUv9qulmESzjb6NCpJQ/OMBlY8eWiSau+Jvu8AMfpV2ce31T6I9Hhy+AStf6oPkg==;EndpointSuffix=core.windows.net
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)


        blob_client.upload_blob(file.read())
        blob_url = blob_client.url
        print(blob_url)

        # data = {'business_name': business_name, 'image_url': blob_url}
        data = {'image_url': blob_url}
        services_collection.insert_one(data)
 

        
        return blob_url, 200 


    except Exception as e:
        return str(e), 500

@app.route('/uploadmultipleimages', methods = ["POST"])
def upload_multiple_image():
    try:

        business_name = request.form['business_name']

        blob_urls = []
        for file in request.files.getlist('image'):
            filename = file.filename
            file_extension = filename.split('.')[-1]
            blob_name = str(timestamp) + '_' + filename
            blob_client = container_client.get_blob_client(blob_name)

            blob_client.upload_blob(file.read())
            blob_urls.append(blob_client.url)

            data = {'business_name': business_name, 'image_urls': blob_urls}
            services_collection.insert_one(data)

        return {'blob_urls': blob_urls}, 200

    except Exception as e:
        return str(e), 500

########################################################
################ ask the community #####################
########################################################

@app.route('/askcommunity',methods=["GET"])
def ask_community():
    try:
        data = list(askcommunity.find())
        for collection in data:
            collection["_id"]= str(collection["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
        
    except:
        return Response(response = json.dumps({"message":"no data available"}),status = 500,mimetype="application/json")

################ ask the community by id #####################  

@app.route('/askcommunity/<uid>', methods=["GET"])
def ask_community_id(uid):
    try:
        data = askcommunity.find_one({"business_uid": uid})
        if data is None:
            # Return an empty data list if business_uid doesn't match
            data = {"_id": "no data", "business_uid": uid, "data": []}
        else:
            data["_id"] = str(data["_id"])
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as e:
        print("hitted exemption {}".format(e))
        return Response(response=json.dumps({"message": "not found"}), status=500, mimetype="application/json")

    



if __name__ == '__main__':
    app.run(debug=True)
