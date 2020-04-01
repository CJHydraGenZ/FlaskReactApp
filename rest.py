from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId
import json

# app = Flask(__name__)
# app.config('MONGO_DBNAME') = 'dbapi'
# app.config('MONGO_URI') = 'mongodb://localhost:27017/dbapi'
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'dbapi'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dbapi'

mongo = PyMongo(app)
CORS(app)

col = mongo.db.reactapi


@app.route('/', methods=['GET', 'POST'])
def getpost():
    if request.method == 'GET':
        data = []
        for i in col.find():
            data.append(
                {'_id': str(ObjectId(i['_id'])), 'nama': i['nama'], 'email': i['email'], 'password': i['password']})
        return jsonify(data)
    elif request.method == 'POST':
        id = col.insert(
            {'nama': request.json['nama'], 'email': request.json['email'], 'password': request.json['password']})
        return jsonify({"id": str(ObjectId(id)), "message": "insert success full"})


@app.route('/<id>', methods=['DELETE', 'PUT'])
def deleteput(id):
    if request.method == 'DELETE':
        col.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'deleted'})
    elif request.method == 'PUT':
        col.update({"_id": ObjectId(id)}, {"$set": {
            "nama": request.json["nama"],
            "email": request.json["email"],
            "password": request.json["password"]
        }})

        # col.update({'_id': str(ObjectId(id))}, {"$set": {
        #     "nama": request.json["nama"],
        #     "email": request.json["email"],
        #     "password": request.json["password"]
        # }})
        return jsonify({"message": "update"})


if __name__ == '__main__':
    app.run(debug=True)
