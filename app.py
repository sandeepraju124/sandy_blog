import json

import pymongo
from flask import Flask
from flask import render_template, request, Response

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['sandeep']
app = Flask(__name__)
# db = client['sandeep']
collection = db.employeeenformation
record = {
    "sandeep": "smart",
    "sai": "vijilint",
    "fuck": "bohut hard"
}


#
# collection.insert_one(record)

# db.allstores.insert_one(record)

# @app.route('/')
# def home():
#     return render_template('index.html')


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


@app.route('/layer1', methods=['GET', 'POST'])
def layer1():
    try:
        data = list(db.layer1.find())
        response = []
        for i in data:
            i['_id'] = str(i['_id'])
            response.append(i)
        return Response(mimetype="application/json", status=500,
                        response=json.dumps({"data": data})

                        )
    except Exception as e:
        # print(e)
        return e


@app.route('/api/', subdomain='api')
def courses():
    return "under practice subdomain."


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.form.get('name')
        print(data)
        print('hit')
    return render_template('test.html')


@app.route('/insertone', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        return "inserted data"

    return 'data not get'


if __name__ == '__main__':
    app.run(port=80, debug=True)
