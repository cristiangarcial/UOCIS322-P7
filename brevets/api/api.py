from flask import Flask, request, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps, loads
import os
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import time
from passlib.hash import sha256_crypt as pwd_context

app = Flask(__name__)
api = Api(app)
SECRET_KEY = 'hotdog@#$'

def generate_auth_token(expiration=600):
   s = Serializer(SECRET_KEY, expires_in=expiration)
   return s.dumps({'id': 5, 'name': 'Ryan'})

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return "Expired token!"    # valid token, but expired
    except BadSignature:
        return "Invalid token!"    # invalid token
    return f"Success! Welcome {data['username']}."

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

def csv_format(brevet_data):
    return_csv = ",".join(list(brevet_data[0].keys())) + "\n"
    for i in brevet_data:
        return_csv += ",".join(i.values()) + "\n"
    return return_csv

class listAll(Resource):
    def get(self, dtype="JSON"):
        topk = request.args.get('dtype', default=-1, type=int)
        token = request.args.get('token', type=str)
        if verify_auth_token(token):
            if topk < -1 or topk is None:
                topk = db.tododb.count()
            if topk == -1:
                brevet_data = db.tododb.find({}, {"_id": 0, "open": 1, "close": 1}) 
            else:
                brevet_data = db.tododb.find({}, {"_id": 0, "open": 1, "close": 1}).limit(topk) 
            if dtype == 'csv':
                    return csv_format(brevet_data)
            return loads(dumps(brevet_data))
        else:
            return {'response': 'error'}, 401

class listOpenOnly(Resource):
    def get(self, dtype="JSON"):
        topk = request.args.get('top', default=-1, type=int)
        token = request.args.get('token', type=str)
        if verify_auth_token(token):  
            if topk < -1 or topk is None:
                topk = db.tododb.count();
            if topk == -1:
                brevet_data = db.tododb.find({}, {"_id": 0, "open": 1}) 
            else:
                brevet_data = db.tododb.find({}, {"_id": 0, "open": 1}).limit(topk) 
            if dtype == 'csv':
                    return csv_format(brevet_data)
            return loads(dumps(brevet_data))
        else:
            return {'response': 'error'}, 401

class listCloseOnly(Resource):
    def get(self, dtype="JSON"):
        topk = request.args.get('top', default=-1, type=int)
        token = request.args.get('token', type=str)
        if verify_auth_token(token):
            if verify_auth_token(token):  
            if topk < -1 or topk is None:
                topk = db.tododb.count();
            if topk == -1:
                brevet_data = db.tododb.find({}, {"_id": 0, "close": 1}) 
            else:
                brevet_data = db.tododb.find({}, {"_id": 0, "close": 1}).limit(topk) 
            if dtype == 'csv':
                    return csv_format(brevet_data)
            return loads(dumps(brevet_data))
        else:
            return {'response': 'error'}, 401


class register(Resource):
    def post(self):
        pass

class register(Resource):
    def post(self):
        pass


api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:dtype>')
api.add_resource(register, '/register', '/register/')
api.add_resource(token, '/token', '/token')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
