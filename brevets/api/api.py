from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps, loads
import os

app = Flask(__name__)
api = Api(app)
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
        if topk < -1 or topk > db.tododb.count() or topk is None:
            topk = db.tododb.count();
        if topk == -1:
            brevet_data = db.tododb.find({}, {"_id": 0, "open": 1, "close": 1}) 
        else:
            brevet_data = db.tododb.find({}, {"_id": 0, "open": 1, "close": 1}).limit(topk) 
        if dtype == 'csv':
                return csv_format(brevet_data)
        return loads(dumps(brevet_data))

class listOpenOnly(Resource):
    def get(self, dtype="JSON"):
        topk = request.args.get('top', default=-1, type=int)
        if topk < -1 or topk is None:
            topk = db.tododb.count();
        if topk < -1:
            return "Error" 
        if topk == -1:
            brevet_data = db.tododb.find({}, {"_id": 0, "open": 1}) 
        else:
            brevet_data = db.tododb.find({}, {"_id": 0, "open": 1}).limit(topk) 
        if dtype == 'csv':
                return csv_format(brevet_data)
        return loads(dumps(brevet_data))

class listCloseOnly(Resource):
    def get(self, dtype="JSON"):
        topk = request.args.get('top', default=-1, type=int)
        if topk < -1 or topk is None:
            topk = db.tododb.count();
        if topk < -1:
            return "Error" 
        if topk == -1:
            brevet_data = db.tododb.find({}, {"_id": 0, "close": 1}) 
        else:
            brevet_data = db.tododb.find({}, {"_id": 0, "close": 1}).limit(topk) 
        if dtype == 'csv':
                return csv_format(brevet_data)
        return loads(dumps(brevet_data))

api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:dtype>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
