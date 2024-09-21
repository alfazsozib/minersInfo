from flask import Flask, request, jsonify
import pymongo
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://aspro1141:3j3nuNuRfKgwxslz@miners.cydxp.mongodb.net/?retryWrites=true&w=majority&appName=miners")
db = client['minersInfo']
collection = db['miners']

@app.route('/get_data', methods=['GET'])
def get_data():
    coin = request.args.get('coin')
    electricity_fee = request.args.get('electricity_fee')

    if not coin or not electricity_fee:
        return jsonify({"error": "Please provide both 'coin' and 'electricity_fee' parameters."}), 400

    try:
        results = collection.find({
            "Coin": coin,
            "User Electricity Fee": electricity_fee
        })
        
        # Convert results to a list and handle ObjectId
        data_list = []
        for result in results:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
            data_list.append(result)
        
        return jsonify(data_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
