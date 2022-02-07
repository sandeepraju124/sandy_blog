from flask import Flask,render_template,url_for,request,redirect,flash
import json
import pymongo
from bson import json_util, ObjectId
from flask import Flask,jsonify

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['sandeep']
app = Flask(__name__)
# db = client['sandeep']
collection= db.employeeenformation
record = {
    "sandeep":"smart",
    "sai":"vijilint",
    "fuck":"bohut hard"
}
#
# collection.insert_one(record)

# db.allstores.insert_one(record)

# @app.route('/')
# def home():
#     return render_template('index.html')



@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # content = request.get_json(force = True)
        data = request.form.get("email")
        # name = content['name']
        # age = content['age']
        # print(content)
        # print(name)
        # print(age)
        print(data)
        print('hit')

        # collecteddata = json.load(data)
        # collection.insert_one(content)
        collection.insert_one({"email":data})
        return "inserted data"
    return render_template('index.html')


@app.route('/layer1',methods=['GET','POST'])
def layer1():
    data =db.layer1.find()
    print(data)
    # jsondata = jsonify([todo for todo in data])
    # print(jsondata)
    for i in data:
        print(i)


    return 'layer1'


@app.route('/api/', subdomain ='api')
def courses():
    return "under practice subdomain."


@app.route('/test',methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.form.get('name')
        print(data)
        print('hit')
    return render_template('test.html')

@app.route('/insertone',methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # content = request.get_json(force = True)
        data = request.form.get('email')
        # name = content['name']
        # age = content['age']
        # print(content)
        # print(name)
        # print(age)
        print(data)
        # collecteddata = json.load(data)
        # collection.insert_one(content)
        return "inserted data"

    return 'data not get'
if __name__ == '__main__':
    # website_url = 'vibhu.gfg:5000'
    # app.config['SERVER_NAME'] = website_url
    app.run(debug=True)