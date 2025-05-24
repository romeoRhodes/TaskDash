from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your-secure-secret-key'
jwt = JWTManager(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['task_dashboard']
tasks_collection = db['tasks']

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'password123':
        token = create_access_token(identity=data['username'])
        return jsonify(access_token=token)
    return jsonify(msg='Bad credentials'), 401

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = list(tasks_collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    result = tasks_collection.insert_one(data)
    return jsonify(msg='Task added', id=str(result.inserted_id))

@app.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': data})
    return jsonify(msg='Task updated')

@app.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return jsonify(msg='Task deleted')

if __name__ == '__main__':
    app.run(debug=True)
