from json import dumps
import os
import pymongo
from flask import Flask, json, jsonify
from flask import render_template, request, Response
from bson.objectid import ObjectId
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
import time
from datetime import datetime
import uuid
import pytz
import psycopg2


# client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
client = pymongo.MongoClient("mongodb+srv://sAdmin:Astrophile_da0515@sr1.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000")
# client = pymongo.MongoClient("mongodb://sr2:RDbkYdz71xf7JNWS1xVsPhWB3L1jTBdfDTBe5HscwUHqHusxC5qpbTRFsJIdtoTmls1Zwldu27mPACDb2VEnzQ==@sr2.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@sr2@")
db = client['sssv1']
app = Flask(__name__)
# db = client['sandeep']
# collection = db.restaurant
service_comments_collection = db.services_comments
user_collection = db.users
services_collection = db.services
askcommunity = db.ask_community
business_categories_collection = db.business_categories





# Create a text index on the 'business_name & etc' field (search) 
## FYI: we don't neccessarily need to create a new collection for search we can retreive data from services_collection which as all the business details.
services_collection.create_index([
    ("business_name", pymongo.TEXT),
    ("business_description", pymongo.TEXT),
    ("business_uid", pymongo.TEXT),
    ("profile_image", pymongo.TEXT),
    ("category", pymongo.TEXT),
    ("sub_category", pymongo.TEXT)
])



# azure storage details
account_name = 'prometheus1137'
account_key = 'QeCd4oED1ZKVaP0W9ncB7KYUv9qulmESzjb6NCpJQ/OMBlY8eWiSau+Jvu8AMfpV2ce31T6I9Hhy+AStf6oPkg=='
container_name = 'sss'
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

# terms and conditions screen

@app.route('/termsandconditions', methods=['GET'])
def tandc():
    
    return render_template('termconditions.html')



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

# @app.route("/serviceIdForComments/<id>",methods=["GET"])
# def rescommentIdForComments(id):
#     # data = service_comments_collection.find_one(ObjectId(id))
#     data = service_comments_collection.find_one({"serviceid": id})
#     if data is None:
#         return Response(response = json.dumps({"error":"comment not found"}),status=404,mimetype="application/json")
#     # print(data)
#     # for users in data:
#     data["_id"]= str(data["_id"])
#     return Response(response = json.dumps(data),status = 200,mimetype="application/json")

# @app.route("/rescomments/<uid>", methods=["GET"])
# def rescommentIdForComments(uid):
#     # data = service_comments_collection.find_one(ObjectId(id))
#     data = service_comments_collection.find_one({"serviceid": uid})
#     if data is None:
#         return Response(response=json.dumps({"error": "comment not found"}), status=404, mimetype="application/json")
#     # print(data)
#     # for users in data:
#     data["_id"] = str(data["_id"])
#     return Response(response=json.dumps(data), status=200, mimetype="application/json")

@app.route('/rescomments/<uid>', methods=["GET"])
def rescommentIdForComments(uid):
    try:
        data = service_comments_collection.find_one({"business_uid": uid})
        if data is None:
            # Return an empty data list if serviceid doesn't match
            data = {"_id": "no data", "business_uid": uid, "data": []}
        else:
            data["_id"] = str(data["_id"])
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as e:
        print("Exception occurred: {}".format(e))
        return Response(response=json.dumps({"message": "not found"}), status=500, mimetype="application/json")




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
        # print("hitted get in user")
        data = list(user_collection.find())
        # print(data)
        for users in data:
            users["_id"]= str(users["_id"])
        return Response(response = json.dumps(data),status = 200,mimetype="application/json")
    elif request.method=='POST':
        if "dp" not in request.files:
            # print("if statement")
            blob_url = 0
        else:
            # print("hitted post in user")
            dp = request.files["dp"]

            # Extract the file extension from the uploaded image
            filename, ext = os.path.splitext(dp.filename)

            blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=mussolini;AccountKey=C/bpeOJzdZwixWwD04pWtGKnmu7Grb6JjL5jnuDBfxkiYvMwniDIr6gTD3CeZECkXQqFlAGx6+HR+AStQeh4fQ==;EndpointSuffix=core.windows.net")
            container_client = blob_service_client.get_container_client("sss")
            random_guid = str(uuid.uuid4())
            blob_name = random_guid + ext
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(dp, content_settings = ContentSettings(content_type="image/jpeg"))

            #  blob_client.upload_blob(dp)
            blob_url = blob_client.url 
            print(blob_url)


        name = request.form['name']
        username = request.form['username']
        email = request.form["email"]
        # dp = request.form["dp"]
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
                'dp':blob_url,
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
        # return Response(dumps({'id': str(result.inserted_id)}), headers=headers)



##########      GET only 1 user by providing user id(GET) and update user data(PUT)      #################

@app.route("/user/<userid>",methods=["GET","PUT"])
def singleuserid(userid):
    if request.method=='GET':
        try:
            data = user_collection.find_one({ "userid":userid})
            
            # for users in data:
            data["_id"]= str(data["_id"])
            return Response(response = json.dumps(data),status = 200,mimetype="application/json")
        except Exception as e:
                print("hitted exemption {}".format(e))
                return Response(response=json.dumps({"message":"data not send"}),status = 500,mimetype="application/json")
        
    elif request.method=='PUT':
        try:
            # Check if the user exists
            existing_user = user_collection.find_one({"userid": userid})
            if existing_user is None:
                return Response(response=json.dumps({"message": "User not found"}), status=404, mimetype="application/json")

            # Get the updated data from the request
            updated_data = {}
            if "name" in request.form:
                updated_data["name"] = request.form["name"]
            if "username" in request.form:
                updated_data["username"] = request.form["username"]
            if "email" in request.form:
                updated_data["email"] = request.form["email"]
            if "street" in request.form:
                existing_user["address"]["street"] = request.form["street"]
            if "state" in request.form:
                existing_user["address"]["state"] = request.form["state"]
            if "zipcode" in request.form:
                existing_user["zipcode"] = request.form["zipcode"]
            if "lat" in request.form:
                existing_user["address"]["geo"]["lat"] = request.form["lat"]
            if "lng" in request.form:
                existing_user["address"]["geo"]["lng"] = request.form["lng"]

            # Handle file upload
            if "dp" in request.files:
                dp = request.files["dp"]
                filename, ext = os.path.splitext(dp.filename)
                blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=mussolini;AccountKey=C/bpeOJzdZwixWwD04pWtGKnmu7Grb6JjL5jnuDBfxkiYvMwniDIr6gTD3CeZECkXQqFlAGx6+HR+AStQeh4fQ==;EndpointSuffix=core.windows.net")
                container_client = blob_service_client.get_container_client("sss")
                random_guid = str(uuid.uuid4())
                blob_name = random_guid + ext
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(dp, content_settings = ContentSettings(content_type="image/jpeg"))

                #  blob_client.upload_blob(dp)
                blob_url = blob_client.url 
                print(blob_url)
                existing_user["dp"] = blob_url

            # Update the user's fields
            existing_user.update(updated_data)

            # Save the updated user
            # user_collection.update_one({"userid": userid}, {"$set": existing_user})

            user_collection.update_one({"userid": userid}, {"$set": existing_user})

            return Response(response=json.dumps({"message": "User updated successfully"}), status=200, mimetype="application/json")

        except Exception as e:
            print("Exception occurred: {}".format(e))
            return Response(response=json.dumps({"message": "Failed to update user"}), status=500, mimetype="application/json")


# //////////////////// edit user /////////////////////////////

# @app.route("/edituser/<userid>", methods=["PUT"])
# def edit_user(userid):
#     try:
#         # Check if the user exists
#         existing_user = user_collection.find_one({"userid": userid})
#         print(existing_user)
#         if existing_user is None:
#             return Response(response=json.dumps({"message": "User not found"}), status=404, mimetype="application/json")

#         # Get the updated data from the request
#         updated_data = request.get_json()
#         print(updated_data)

#         # Update the user's fields
#         if "name" in updated_data:
#             existing_user["name"] = updated_data["name"]
#         if "username" in updated_data:
#             existing_user["username"] = updated_data["username"]
#         if "email" in updated_data:
#             existing_user["email"] = updated_data["email"]
#         if "street" in updated_data:
#             existing_user["address"]["street"] = updated_data["street"]
#         if "state" in updated_data:
#             existing_user["address"]["state"] = updated_data["state"]
#         if "zipcode" in updated_data:
#             existing_user["zipcode"] = updated_data["zipcode"]
#         if "lat" in updated_data:
#             existing_user["address"]["geo"]["lat"] = updated_data["lat"]
#         if "lng" in updated_data:
#             existing_user["address"]["geo"]["lng"] = updated_data["lng"]

#         # Save the updated user
#         user_collection.update_one({"userid": userid}, {"$set": existing_user})

#         return Response(response=json.dumps({"message": "User updated successfully"}), status=200, mimetype="application/json")

#     except Exception as e:
#         print("Exception occurred: {}".format(e))
#         return Response(response=json.dumps({"message": "Failed to update user"}), status=500, mimetype="application/json")


####################################################################
 #################### below is the endpoint for Search ######################### 
####################################################################
        

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get("query")
        # Use the $text operator for text search
        services_data = list(services_collection.find({
            "$text": {
                "$search": query,
                "$language": "english",
                "$caseSensitive": False,
            }
        }))

        # Calculate the average rating for each service and include location
        for service in services_data:
            service_id = service['business_uid']
            comments = list(service_comments_collection.find({"business_uid": service_id}))
            # Extract ratings from the nested 'reviews' field
            ratings = [review['rating'] for comment in comments for review in comment.get('reviews', []) if 'rating' in review]
            if ratings:
                average_rating = sum(ratings) / len(ratings)
                service['average_rating'] = round(average_rating, 1)
            else:
                service['average_rating'] = 0  # No ratings available
            # Include the location field from the service document
            service['country'] = service.get('country')

        for result in services_data:
            result["_id"] = str(result["_id"])

        return Response(response=json.dumps(services_data), status=200, mimetype="application/json")

    except Exception as e:
        print(f"Search error: {e}")  # Debug print
        return Response(response=json.dumps({"message": "Error in search"}), status=500, mimetype="application/json")


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
        
    # if request.method=='POST':
    #     try:
    #         business_name = request.form['business_name']
    #         business_description = request.form['business_description']
    #         contact_information = request.form['contact_information']
    #         country = request.form['country']
    #         category = request.form['category']
    #         sub_category = request.form['sub_category']
    #         latitude = request.form['latitude']
    #         longitude = request.form['longitude']
    #         profile_image = request.files['profile_image']


    #         service_fields = {}
    #         blob_urls = []

    #         if business_name:
    #             service_fields["business_name"] = business_name
    #         if business_description:
    #             service_fields["business_description"] = business_description
    #         if contact_information:
    #             service_fields["contact_information"] = contact_information
    #         if country:
    #             service_fields["country"] = country
    #         if category:
    #             service_fields["category"] = category
    #         if sub_category:
    #             service_fields["sub_category"] = sub_category
    #         if latitude:
    #             service_fields["latitude"] = latitude
    #         if longitude:
    #             service_fields["longitude"] = longitude

    #         if 'profile_image' in request.files:
    #             profile_image = request.files['profile_image']
    #             filename = profile_image.filename
    #             print("filename")
    #             print(filename)
    #             print(timestamp)
    #             blob_name = str(timestamp) + '_' + filename
    #             blob_client = container_client.get_blob_client(blob_name)
    #             blob_client.upload_blob(profile_image.read())
    #             blob_url = blob_client.url
    #             service_fields["profile_image"] = blob_url




    #         if 'images' in request.files:
    #             for file in request.files.getlist('images'):
    #                 filename = file.filename
    #                 file_extension = filename.split('.')[-1]
    #                 blob_name = str(timestamp) + '_' + filename
    #                 blob_client = container_client.get_blob_client(blob_name)

    #                 blob_client.upload_blob(file.read())
    #                 blob_urls.append(blob_client.url)

    #         service_fields["images"] = blob_urls
    #         # if sub_catagory:
    #         #     service_fields["images"] = sub_catagory


    #         services_collection.insert_one(service_fields)
    #         print("blob_urls {}".format(blob_urls))

    #         return jsonify({'message': 'Service added successfully.'}), 200
    
        # except Exception as e:
        #     return  jsonify({'message': f'Error adding service: {str(e)}'}), 500

# -----------------------------------------------------------------------
#       depcricated below api and implemented same for postgres
# -----------------------------------------------------------------------

# ################ get business by category ######################
# @app.route("/category/<category>",methods=["GET"])
# def category(category):
#     try:
#         data = list(services_collection.find({"category": category}))
#         for users in data:
#             users["_id"]= str(users["_id"])
#         # categories = set(service['category'] for service in data)
#         subcategories = set(service['sub_category'] for service in data)
#         response_data = {"services": data,"subcategories": list(subcategories)}
#         return Response(response=json.dumps(response_data), status=200, mimetype="application/json")
#     except Exception as e:
#             print("hitted exemption {}".format(e))
#             return Response(response=json.dumps({"message":"not found"}),status = 500,mimetype="application/json")
    
# ################ get business by subcategory ######################
# from bson import ObjectId

# @app.route("/subcategory/<subcategory>", methods=["GET"])
# def subcategory(subcategory):
#     try:
#         data = list(services_collection.find({"sub_category": subcategory}))
#         filtered_data = []
#         for user in data:
#             filtered_user = {
#                 # here we have only taken selected fields ignoring _id, images, etc add below if you want to add extar fields
#                 "business_name": user.get("business_name"),
#                 "business_uid": str(user.get("business_uid")),  # Convert ObjectId to string
#                 "contact_information": user.get("contact_information"),
#                 "profile_image": user.get("profile_image"),
#                 "latitude": user.get("latitude"),
#                 "longitude": user.get("longitude"),
#                 "business_description": user.get("business_description"),
#                 "reviews_length": 0
#             }
#             uid = user.get("business_uid")
#             comment_data = service_comments_collection.find_one({"business_uid": uid})
#             if comment_data:
#                 reviews = comment_data.get("reviews", [])
#                 overall_rating = sum(review.get("rating", 0) for review in reviews) / len(reviews) if reviews else 0
#                 overall_rating = round(overall_rating, 1)
#                 filtered_user["reviews_length"] = len(reviews)
#             else:
#                 overall_rating = 0
#             filtered_user["overall_rating"] = overall_rating
#             filtered_data.append(filtered_user)
#         return Response(response=json.dumps(filtered_data), status=200, mimetype="application/json")
#     except Exception as e:
#         print("hitted exemption {}".format(e))
#         return Response(response=json.dumps({"message": "not found"}), status=500, mimetype="application/json")


# -----------------------------------------------------------------------

# -----------------------------------------------------------------------


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
    



    

########################################################
################ user activity by userid #####################
########################################################
    

@app.route('/user_activities/<user_id>', methods=['GET'])
def get_user_activities(user_id):
    try:
        # Fetch user activities from different collections
        comments = list(service_comments_collection.find({"reviews.user_id": user_id}))
        questions = list(askcommunity.find({"data.qdetails.userid": user_id}))
        all_answers = list(askcommunity.find({}))
        # print(services)

        # Fetch business data from services_collection
        businesses = {document['business_uid']: document['business_name'] for document in services_collection.find({})}

        # Process the fetched data to get user's activities
        user_comments = [
            {**review, 'business_uid': document['business_uid'], 'business_name': businesses.get(document['business_uid'])} 
            for document in comments for review in document.get('reviews', []) 
            if review.get('user_id') == user_id
        ]
        user_questions = [
            {**item, 'business_uid': document['business_uid'], 'business_name': businesses.get(document['business_uid'])} 
            for document in questions for item in document.get('data', []) 
            if item.get('qdetails', {}).get('userid') == user_id
        ]
        user_answers = [
            {**answer, 'business_uid': document['business_uid'], 'business_name': businesses.get(document['business_uid'])} 
            for document in all_answers for item in document.get('data', []) 
            for answer in item.get('answers', []) 
            if answer.get('adetails', {}).get('userid') == user_id
        ]

        # Combine the activities
        activities = {
            "comments": user_comments,
            "questions": user_questions,
            "answers": user_answers
        }

        return jsonify(activities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            data = {"_id": "", "business_uid": uid, "reviews": [], "rating_count": {
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
            for comment in data.get("reviews", []):
                user_id = comment.get("user_id")
                user_data = user_collection.find_one({"userid": user_id})
                if user_data:
                    comment["username"] = user_data.get("username", "Unknown User")
                    comment["dp"] = user_data.get("dp", "")

            # Calculate the ratings
            rating_count = {
                "5": 0,
                "4": 0,
                "3": 0,
                "2": 0,
                "1": 0
            }
            total_rating = 0

            for comment in data.get("reviews", []):
                rating = comment.get("rating")
                if rating:
                    total_rating += rating
                    rating_count[str(rating)] += 1

            data["rating_count"] = rating_count
            data["overall_rating"] = round(total_rating / len(data["reviews"]), 1) if data["reviews"] else 0

        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"message": "Error fetching comments"}), status=500, mimetype="application/json")

################ post user comment ######################


@app.route("/postcomment", methods=["POST"])
def postcomment():
    try:
        rating = int(request.form['rating'])
        user_id = request.form['user_id']
        business_uid = request.form['business_uid']
        selected_suggestions = request.form.get('selected_suggestions', '').split(' + ')  # Split the string into a list
        user_reviews = request.form.get('user_reviews', '').split(' + ')   
        
        # Fetch the username from the user_collection
        user_data = user_collection.find_one({"userid": user_id})
        username = user_data["username"] if user_data else "Unknown User"
        
        # Set the timezone to 'Asia/Kolkata' for Indian Standard Time
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone).isoformat()

        # Initialize the combined_review with the selected suggestions
        combined_review = "\n".join(suggestion for suggestion in selected_suggestions)

        # If there are user reviews, append them to the combined_review
        if user_reviews:
            combined_review += "\n"  # Add a newline if there are both suggestions and reviews
            combined_review += "\n".join(review for review in user_reviews)

        # Generate a unique review_id
        review_id = str(uuid.uuid4())

        # Create a new comment object
        new_comment = {
            "review_id": review_id,
            "rating": rating,
            "comment": combined_review,
            "user_id": user_id,
            "username": username,
            "created_at": current_time
        }

        # Check if business_uid exists in the collection
        existing_business = service_comments_collection.find_one({"business_uid": business_uid})

        if existing_business:
            # Update the reviews list in the existing business document
            service_comments_collection.update_one(
                {"business_uid": business_uid},
                {"$push": {"reviews": new_comment}},
                upsert=True  # Create a new document if it doesn't exist
            )
        else:
            # Create a new collection and insert the document
            new_business = {
                "business_uid": business_uid,
                "reviews": [new_comment]
            }
            service_comments_collection.insert_one(new_business)

        return "done"

    except Exception as e:
        return str(e),  500
    
 ################### Edit comment Endpoint ##################
    

    
@app.route("/editcomment", methods=["PUT"])
def edit_comment():
    try:
        business_uid = request.form['business_uid']
        review_id = request.form['review_id']
        user_id = request.form['user_id']  # Assuming the user_id is sent in the request
        new_rating = int(request.form['rating'])
        new_review = request.form['review']
        
        # Fetch the specific review to check if the user_id matches
        review = service_comments_collection.find_one(
            {"business_uid": business_uid, "reviews.review_id": review_id},
            {"reviews.$":  1}
        )

        # Set the timezone to 'Asia/Kolkata' for Indian Standard Time
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone).isoformat()

        # If the review exists and the user_id matches, proceed with the update
        if review and review.get('reviews', [{}])[0].get('user_id') == user_id:
            # Update the specific review in the business document using the $ positional operator
            result = service_comments_collection.update_one(
                {"business_uid": business_uid, "reviews.review_id": review_id},
                {"$set": {
                    "reviews.$.rating": new_rating,  
                    "reviews.$.comment": new_review,  # Use the new combined review string
                    "reviews.$.updated_at": current_time  # Add the current timestamp
                }}
            )
            
            if result.matched_count ==  0:
                return jsonify({"error": "Business or review not found"}),  404
            
            return jsonify({"message": "Review updated successfully"}),  200
        else:
            return jsonify({"error": "Unauthorized or review not found"}),  403

    except Exception as e:
        return jsonify({"error": str(e)}),  500

####################### Delete Comment Endpoint  ###########################


@app.route("/deletecomment", methods=["DELETE"])
def delete_comment():
    try:
        business_uid = request.form['business_uid']
        review_id = request.form['review_id']
        user_id = request.form['user_id']  # Assuming the user_id is sent in the request

        # Fetch the specific review to check if the user_id matches
        review = service_comments_collection.find_one(
            {"business_uid": business_uid, "reviews.review_id": review_id},
            {"reviews.$": 1}
        )

        # If the review exists and the user_id matches, proceed with the deletion
        if review and review.get('reviews', [{}])[0].get('user_id') == user_id:
            # Delete the specific review from the business document
            result = service_comments_collection.update_one(
                {"business_uid": business_uid},
                {"$pull": {"reviews": {"review_id": review_id}}}
            )

            if result.modified_count == 0:
                return jsonify({"error": "Review not found or could not be deleted"}), 404

            return jsonify({"message": "Review deleted successfully"}), 200
        else:
            return jsonify({"error": "Unauthorized or review not found"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



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

            print(data),
        else:
            data["_id"] = str(data["_id"])
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as e:
        print("hitted exemption {}".format(e))
        return Response(response=json.dumps({"message": "not found"}), status=500, mimetype="application/json")


# //////////////// post question Ask community /////////////////////

    
@app.route('/post_question', methods=['POST'])
def post_question():
    try:
        # Parse the request data
        business_uid = request.form.get('business_uid')
        question_text = request.form.get('question')
        userid = request.form.get('userid')

        if not business_uid or not question_text or not userid:
            return jsonify({"error": "Missing required data"}), 400

        # Find the document with the specified business_uid
        business_data = askcommunity.find_one({"business_uid": business_uid})
        # print(business_data)

        if business_data is None:
            # If the business_uid doesn't exist, create a new document
            new_document = {
                "business_uid": business_uid,
                "data": []
            }
            askcommunity.insert_one(new_document)
            business_data = new_document

            # Set the timezone to 'Asia/Kolkata' for Indian Standard Time
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone).isoformat()


        # Create a new question document
        question_id = str(uuid.uuid4().hex[:10])
        new_question = {
            "qdetails": {
                "created_at": current_time,  # You can set the current timestamp here
                "questionid": question_id,  # Generate a unique question ID
                "userid": userid,
            },
            "question": question_text,
            "answers": []  # Initially, there are no answers for the new question
        }

        # Add the new question to the 'data' array in the document
        business_data['data'].append(new_question)

        # Update the document in the database
        askcommunity.update_one({"_id": business_data["_id"]}, {"$set": business_data})

        return jsonify({"message": "Question posted successfully", "questionid": question_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    



######################## Below Edit question endpoint ##########
@app.route('/edit_question', methods=['PUT'])
def edit_question():
    try:
        # Parse the request data
        business_uid = request.form.get('business_uid')
        question_id = request.form.get('questionid')
        new_question_text = request.form.get('new_question')
        userid = request.form.get('userid')  # The ID of the user attempting to edit the question

        if not business_uid or not question_id or not new_question_text or not userid:
            return jsonify({"error": "Missing required data"}), 400

        # Find the document with the specified business_uid
        business_data = askcommunity.find_one({"business_uid": business_uid})

        if business_data is None:
            return jsonify({"error": "Business data not found"}), 404
        
        # Set the timezone to 'Asia/Kolkata' for Indian Standard Time
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone).isoformat()


        # Check if the question exists and if the userid matches
        question_found = False
        for question in business_data['data']:
            if question['qdetails']['questionid'] == question_id and question['qdetails']['userid'] == userid:
                question_found = True
                question['question'] = new_question_text
                # Update the updated_at timestamp for the question
                question['qdetails']['updated_at'] = current_time
                break

        if not question_found:
            return jsonify({"error": "Question not found or unauthorized"}), 403

        # Update the document in the database
        askcommunity.update_one({"_id": business_data["_id"]}, {"$set": business_data})

        return jsonify({"message": "Question updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    ################## Below delete question Endpoint #################
@app.route('/delete_question', methods=['DELETE'])
def delete_question():
    try:
        # Parse the request data
        question_id = request.form.get('questionid')
        userid = request.form.get('userid')
        business_uid = request.form.get('business_uid')  # Get business_uid from the request

        if not question_id or not userid or not business_uid:  # Check for business_uid as well
            return jsonify({"error": "Missing required data"}), 400

        # Find the document that contains the question with the specified question_id and business_uid
        business_data = askcommunity.find_one({"business_uid": business_uid, "data.qdetails.questionid": question_id})

        if business_data:
            # Check if the question exists and if the userid matches
            question_found = False
            for question in business_data['data']:
                if question['qdetails']['questionid'] == question_id and question['qdetails']['userid'] == userid:
                    question_found = True
                    # Remove the question from the 'data' array
                    business_data['data'].remove(question)
                    break

            if not question_found:
                return jsonify({"error": "Question not found or unauthorized"}), 403

            # Update the document in the database
            askcommunity.update_one({"_id": business_data["_id"]}, {"$set": business_data})

            return jsonify({"message": "Question deleted successfully"}), 200
        else:
            return jsonify({"error": "Question not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
# //////////////// post answer Ask community /////////////////////

@app.route('/post_answer', methods=['POST'])
def post_answer():
    try:
        # Parse the request data
        question_id = request.form.get('questionid')
        answer_text = request.form.get('answer')
        userid = request.form.get('userid')

        if not question_id or not answer_text or not userid:
            return jsonify({"error": "Missing required data"}), 400

        # Find the document that contains the question with the specified question_id
        business_data = askcommunity.find_one({"data.qdetails.questionid": question_id})

        if business_data:
            # Generate a unique answer ID and take the first 10 digits
            answer_id = str(uuid.uuid4().hex)[:10]

            # Set the timezone to 'Asia/Kolkata' for Indian Standard Time
            timezone = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(timezone).isoformat()


            # Create a new answer document
            new_answer = {
                "adetails": {
                    "created_at": current_time,  # Set the current timestamp here
                    "userid": userid,
                    "answerid": answer_id,  # Include the answer ID here
                },
                "answer": answer_text
            }

            # Add the new answer to the question's 'answers' array
            for question in business_data['data']:
                if question['qdetails']['questionid'] == question_id:
                    question['answers'].append(new_answer)

                    # Update the document in the database
                    askcommunity.update_one({"_id": business_data["_id"]}, {"$set": business_data})

                    return jsonify({"message": "Answer posted successfully"}), 200

        return jsonify({"error": "Question not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    



########### Endpoint for Edit_Answer ########
    
@app.route('/edit_answer', methods=['PUT'])
def edit_answer():
    try:
        business_uid = request.form.get('business_uid')  
        question_id = request.form.get('questionid')
        answer_id = request.form.get('answerid')
        new_answer_text = request.form.get('new_answer')
        userid = request.form.get('userid')

        if not business_uid or not question_id or not answer_id or not new_answer_text or not userid: 
            return jsonify({"error": "Missing required data"}), 400

        business_data = askcommunity.find_one({"business_uid": business_uid, "data.qdetails.questionid": question_id})  
        # Set the timezone to 'Asia/Kolkata' for Indian Standard Time
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone).isoformat()


        if business_data:
            for question in business_data['data']:
                if question['qdetails']['questionid'] == question_id:
                    for answer in question['answers']:
                        if answer['adetails']['answerid'] == answer_id and answer['adetails']['userid'] == userid:
                            answer['answer'] = new_answer_text
                            # Update the updated_at timestamp for the answer
                            answer['adetails']['updated_at'] = current_time,
                            askcommunity.update_one({"_id": business_data["_id"]}, {"$set": business_data})
                            return jsonify({"message": "Answer updated successfully"}), 200
            return jsonify({"error": "Answer not found or unauthorized"}), 403
        else:
            return jsonify({"error": "Question not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


######## Endpoint for Delete_Answer #########
    
@app.route('/delete_answer', methods=['DELETE'])
def delete_answer():
    try:
        business_uid = request.form.get('business_uid')
        question_id = request.form.get('questionid')
        answer_id = request.form.get('answerid')
        userid = request.form.get('userid')

        if not business_uid or not question_id or not answer_id or not userid:  
            return jsonify({"error": "Missing required data"}), 400

        business_data = askcommunity.find_one({"business_uid": business_uid, "data.qdetails.questionid": question_id})  


        if business_data:
            for question in business_data['data']:
                if question['qdetails']['questionid'] == question_id:
                    for answer in question['answers']:
                        if answer['adetails']['answerid'] == answer_id and answer['adetails']['userid'] == userid:
                            question['answers'].remove(answer)
                            askcommunity.update_one({"_id": business_data["_id"]}, {"$set": business_data})
                            return jsonify({"message": "Answer deleted successfully"}), 200
            return jsonify({"error": "Answer not found or unauthorized"}), 403
        else:
            return jsonify({"error": "Question not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/overall_rating/<business_uid>', methods = ["GET"])
def overall_rating(business_uid):
    # uid = user.get("business_uid")
    try:
        comment_data = service_comments_collection.find_one({"business_uid": business_uid})
        print("")
        if comment_data:
            reviews = comment_data.get("reviews", [])
            overall_rating = sum(review.get("rating", 0) for review in reviews) / len(reviews) if reviews else 0
            reviews_count = len(reviews)
            overall_rating = round(overall_rating, 1)
            return jsonify({"overall_rating": overall_rating, "reviews_count": reviews_count}), 200
            # filtered_user["reviews_length"] = len(reviews)
        else:
            # overall_rating = 0
            return jsonify({"message": "No reviews available for this business.", "overall_rating": 0, "reviews_count": 0}), 200
        # return jsonify(overall_rating), 200
    except KeyError:
        return jsonify({"message": "Key error occurred. Invalid data structure."}), 500
    except ZeroDivisionError:
        return jsonify({"message": "No reviews available for this business."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/business_categories', methods=["GET"])
def business_categories():
    try:
        cursor = list(business_categories_collection.find())
        for category in cursor:
            category["_id"] = str(category["_id"])
        return Response(response=json.dumps(cursor), status=200, mimetype="application/json")
    
    except Exception as e:
        return Response(response=json.dumps({"message": str(e)}), status=500, mimetype="application/json")

######################################################
    # POSTGRESS REST APIS
######################################################
    

def execute_query(query, params=None):
    print("called execute_query")
    db_config = {
        'host': 'postgres.cdmy8mee4s8m.us-east-1.rds.amazonaws.com',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': '9912277968'
    }
    try:
        print("try")
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query with optional parameters
        cursor.execute(query, params)
        if any(keyword in query.strip().upper() for keyword in ["INSERT", "UPDATE", "DELETE"]):
            # For INSERT queries, commit the transaction and return None
            connection.commit()
            row_count = cursor.rowcount
            print(f"Rows affected: {row_count}")
            cursor.close()
            connection.close()
            return row_count
        
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        print(column_names)
        cursor.close()
        connection.close()
        result = [dict(zip(column_names, row)) for row in rows]

        return result
    except Exception as e:
        raise e


def upload_to_azure(file,business_uid):
    connection_string = "DefaultEndpointsProtocol=https;AccountName=chambersafe;AccountKey=LU8ZPmbxH6yALstQxEDxCaoPfS3VEWut06bqEOdwxRiukEm7sgQOkLPflx++XGEwOuSnYlvwo1G5+ASt8lszfA==;EndpointSuffix=core.windows.net"
    container_name = "slytherinsafestorage"
    blob_name =  business_uid + "-"+  str(uuid.uuid4())+ os.path.splitext(file.filename)[-1]  # Generate a unique blob name
    print(blob_name)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(file)
    return blob_client.url
 

# Endpoint to retrieve all data from the 'business' table
@app.route('/pg/business', methods=['GET','POST','PATCH'])
def get_business():
    if request.method == 'GET':
        try:
            query = "SELECT * FROM business;"
            result = execute_query(query)
            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    elif request.method == 'POST':
        try:
            data = request.form.to_dict()  # Convert ImmutableMultiDict to a mutable dictionary
            # print(data["business_uid"])
            business_uid = data["business_uid"]
            file = request.files.get("profile_image_url")
            file_url = upload_to_azure(file,business_uid)
            data['profile_image_url'] = file_url
            keys = ', '.join(data.keys())
            values = ', '.join(['%s' for _ in range(len(data))])
            insert_query = f"INSERT INTO business ({keys}) VALUES ({values})"
            execute_query(insert_query, tuple(data.values()))  # Execute the insert query

            return jsonify({'message': 'Business added successfully'})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    elif request.method == 'PATCH':
        print("in patch")
        try:
            data = request.json
            business_uid = data['business_uid']
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE business SET {set_clause} WHERE business_uid = %s"
            params = tuple(data.values()) + (business_uid,)
            result = execute_query(query, params)
            # print(result)
            # print("result")
            if result is not None:
                return jsonify({'message': 'Business updated successfully'})
            else:
                return jsonify({'error': 'Failed to update business'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
# ////////////////////////// testing above methpost method to upload image as well ////////////////

# def upload_to_azure(file,business_uid):
#     connection_string = "DefaultEndpointsProtocol=https;AccountName=chambersafe;AccountKey=LU8ZPmbxH6yALstQxEDxCaoPfS3VEWut06bqEOdwxRiukEm7sgQOkLPflx++XGEwOuSnYlvwo1G5+ASt8lszfA==;EndpointSuffix=core.windows.net"
#     container_name = "slytherinsafestorage"
#     blob_name =  business_uid + "-"+  str(uuid.uuid4())+ os.path.splitext(file.filename)[-1]  # Generate a unique blob name
#     print(blob_name)
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
#     blob_client.upload_blob(file)
#     return blob_client.url
 


# @app.route("/testingdataimageupdate",methods = ['POST'])
# def testingdataimageupdate():
#     try:
#         data = request.form.to_dict()  # Convert ImmutableMultiDict to a mutable dictionary
#         # print(data["business_uid"])
#         business_uid = data["business_uid"]
#         file = request.files.get("profile_image_url")
#         file_url = upload_to_azure(file,business_uid)
#         data['profile_image_url'] = file_url
#         keys = ', '.join(data.keys())
#         values = ', '.join(['%s' for _ in range(len(data))])
#         insert_query = f"INSERT INTO business ({keys}) VALUES ({values})"
#         execute_query(insert_query, tuple(data.values()))  # Execute the insert query

#         return jsonify({'message': 'Business added successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500




# ////////////////////////// testing above methpost method to upload image as well ////////////////

# Endpoint to retrieve filter data by passing params
@app.route('/pg/business/where', methods=['GET'])
def get_category():
    try:
        base_query = "SELECT * FROM business WHERE"
        filters = request.args
        print(f"filters {filters.values()}") #ImmutableMultiDict([('category', 'food')])
        where_clause = " AND ".join([f"{key} = %s" for key in filters.keys()]) # category = %s
        print(f"where_clause {where_clause}")
        full_query = f"{base_query} {where_clause};" if where_clause else f"{base_query} {full_query}"
        result = execute_query(full_query, tuple(filters.values()))


        # query = "SELECT * FROM business WHERE category = '{}';".format(category)
        # result = execute_query(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

@app.route('/pg/business/house-data', methods=['GET'])
def get_house_data():
    try:
        # Use all query parameters directly
        query_params = request.args.to_dict()


        # Define the SQL query
        # WHERE {' AND '.join([f"house.{key} = %s" for key in query_params])}
            # WHERE {' AND '.join([f"house.{key} = %s" for key in query_params])}
        query = f"""
            SELECT *
            FROM house
            JOIN business ON house.business_uid = business.business_uid
            WHERE {' AND '.join([f"house.{key} = %s" for key in query_params])}
            
        """


            
        # Execute the query with parameters
        result = execute_query(query, list(query_params.values()))

        # Return the data as JSON
        return jsonify(result)

    except Exception as e:
        # Handle errors
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to retrieve house data'})



# get data based on lat and lang

@app.route('/pg/business/latlong',methods=['GET'])
def businessforlatlong():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    distance = request.args.get('distance')
    key = request.args.get('key')
    value = request.args.get('value')
    # print(latitude)
    # print(key)

    query = """
    SELECT *
    FROM business
    WHERE ST_DWithin(
        ST_GeographyFromText('POINT(%s %s)'),
        geography(ST_MakePoint(business.longitude, business.latitude)),
        %s
    )
    """

    if key and value:
        query += f"AND business.{key} = %s"

    # Execute the query
    result = execute_query(query, (latitude, longitude, distance, value) if key and value else (latitude, longitude, distance))



    # query = f"""
    # SELECT *
    # FROM business
    # WHERE ST_DWithin(
    #     ST_GeographyFromText('POINT(%s %s)'),
    #     geography(ST_MakePoint(business.longitude, business.latitude)),
    #     %s
    # ) And business.{key} = %s
    # """

    # result = execute_query(query, (latitude, longitude, distance,value))
    # print(result)
    # print("result")
    return jsonify(result)



# search
# API endpoint for searching businesses
@app.route('/pg/search', methods=['GET'])
def search_business():
    query = request.args.get('query')
    count = request.args.get('count', default=None, type=int)  # Get the count parameter
    print(query)
    if not query:
        return jsonify({'error': 'Query parameter "query" is required'}), 400

    # Construct the SQL query to search for businesses
    sql_query = """
        SELECT * FROM business
        WHERE business_name ILIKE %s
    """
    params = ('%' + query + '%',)  # Parameters for the SQL query

    try:
        # Execute the SQL query using the execute_query function
        results = execute_query(sql_query, params)
        
        if count is not None:
            results = results[:count]

        # Serialize the results
        serialized_results = []
        for result in results:
            serialized_results.append({
                'business_name': result['business_name'],
                'business_uid': result['business_uid'],
                # Serialize other fields as needed
            })

        return jsonify(serialized_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

@app.route('/pg/fulltext_search', methods=['GET'])
def fullsearch_business():
    query = request.args.get('query')
    count = request.args.get('count', default=None, type=int) # Get the count parameter

    if not query:
        return jsonify({'error': 'Query parameter "query" is required'}), 400

    # Append the wildcard to the end of the query
    query += ':*'

    # Construct the SQL query to search for businesses
    sql_query = """
        SELECT * FROM business
        WHERE to_tsvector('english', business_name || ' ' || business_description || ' ' || country || ' ' || category || ' ' || sub_category) @@ to_tsquery('english', %s)
    """
    params = (query,)

    try:
        # Execute the SQL query using the execute_query function
        results = execute_query(sql_query, params)
        
        if count is not None:
            results = results[:count]

        # Serialize the results
        serialized_results = []
        for result in results:
            # Fetch the reviews for the business from the service_comments collection
            reviews = service_comments_collection.find_one({"business_uid": result['business_uid']})
            if reviews and 'reviews' in reviews:
                # Calculate the average rating
                total_rating = sum(review['rating'] for review in reviews['reviews'])
                average_rating = total_rating / len(reviews['reviews']) if reviews['reviews'] else 0
            else:
                average_rating = 0

            serialized_results.append({
                'business_name': result['business_name'],
                'business_uid': result['business_uid'],
                'profile_image_url': result['profile_image_url'],
                'latitude': result['latitude'],
                'longitude': result['longitude'],
                'business_description': result['business_description'],
                'country': result['country'],
                'address': result['address'],
                'average_rating': average_rating
                # Serialize other fields as needed
            })

        return jsonify(serialized_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500




######################################################
# |||||||   POSTGRESS REST APIS  |||||||||||
######################################################

if __name__ == '__main__':
    app.run(debug=True)