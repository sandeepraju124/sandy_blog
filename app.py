import json
import pymongo
from flask import Flask, jsonify
from flask import render_template, request, Response

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
# client = pymongo.MongoClient("mongodb://mongodb-flask:BvFOOXd0cOoU9vETxCZsDbaPrwrfcoraV3fTkNoWueaFpD4amKvIsM8Gu42hcviJ2Xfz3qfOShu84hxoVgL5iA==@mongodb-flask.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-flask@")
db = client['sandeep']
app = Flask(__name__)
# db = client['sandeep']
collection = db.employeeenformation



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




dict = [{
"userId": 1,
"id": 1,
"title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
"body": "quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto"
},
{
"userId": 1,
"id": 2,
"title": "qui est esse",
"body": "est rerum tempore vitae sequi sint nihil reprehenderit dolor beatae ea dolores neque fugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis qui aperiam non debitis possimus qui neque nisi nulla"
},
{
"userId": 1,
"id": 3,
"title": "ea molestias quasi exercitationem repellat qui ipsa sit aut",
"body": "et iusto sed quo iure voluptatem occaecati omnis eligendi aut ad voluptatem doloribus vel accusantium quis pariatur molestiae porro eius odio et labore et velit aut"
},
{
"userId": 1,
"id": 4,
"title": "eum et est occaecati",
"body": "ullam et saepe reiciendis voluptatem adipisci sit amet autem assumenda provident rerum culpa quis hic commodi nesciunt rem tenetur doloremque ipsam iure quis sunt voluptatem rerum illo velit"
},
{
"userId": 1,
"id": 5,
"title": "nesciunt quas odio",
"body": "repudiandae veniam quaerat sunt sed alias aut fugiat sit autem sed est voluptatem omnis possimus esse voluptatibus quis est aut tenetur dolor neque"
},
{
"userId": 1,
"id": 6,
"title": "dolorem eum magni eos aperiam quia",
"body": "ut aspernatur corporis harum nihil quis provident sequi mollitia nobis aliquid molestiae perspiciatis et ea nemo ab reprehenderit accusantium quas voluptate dolores velit et doloremque molestiae"
},]


@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify(dict)


# @app.route('/layer1', methods=['GET', 'POST'])
# def layer1():
#     try:
#         data = list(db.layer1.find())
#         response = []
#         for i in data:
#             i['_id'] = str(i['_id'])
#             response.append(i)
#         return Response(mimetype="application/json", status=500,
#                         response=json.dumps({"data": data})
#
#                         )
#     except Exception as e:
#         # print(e)
#         return e
#



if __name__ == '__main__':
    app.run(debug=True)
