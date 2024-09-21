from flask import Flask, request, jsonify
import pymongo
from bson import ObjectId

app = Flask(__name__)
# 0D3B2RH0yAlqoSJJ
# mongodb+srv://aspro1141:3j3nuNuRfKgwxslz@miners.cydxp.mongodb.net/?retryWrites=true&w=majority&appName=miners
# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://anshrv17:0D3B2RH0yAlqoSJJ@miners.na2kt.mongodb.net/?retryWrites=true&w=majority&appName=miners")
db = client['minersInfo']
collection = db['miners']

@app.route('/get_data', methods=['GET'])
def get_data():
    coin = request.args.get('coin')
    electricity_fee = request.args.get('electricity_fee')

    if not electricity_fee:
        return jsonify({"error": "Please provide 'electricity_fee' parameter."}), 400

    try:
        query = {"User Electricity Fee": electricity_fee}

        if coin != "ALL":
            query["Coin"] = coin
        
        results = collection.find(query)

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
