from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://root:example@mongodb:27017/'
mongo = PyMongo(app)


@app.route('/data', methods=['GET', 'POST', 'PUT'])
def handle_data():
    if request.method == 'GET':
        data = mongo.db.data.find_one({'key': 'example'})
        return jsonify({'value': data['value']} if data else {'message': 'Not found'})
    
    elif request.method == 'POST':
        request_data = request.get_json()
        new_value = request_data.get('value')
        mongo.db.data.update_one({'key': 'example'}, {'$set': {'value': new_value}}, upsert=True)
        return jsonify({'message': 'Updated successfully'})
    
    elif request.method == 'PUT':
        request_data = request.get_json()
        key = request_data.get('key')
        value = request_data.get('value')
        mongo.db.data.insert_one({'key': key, 'value': value})
        return jsonify({'message': 'Created successfully'})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
