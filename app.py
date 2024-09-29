import requests
import time
import pandas as pd
import json
import pymongo

def scraper():
    prices = ['0.01', '0.02', '0.03', '0.04', '0.05', '0.06', '0.07', '0.08', '0.09', '0.10', '0.11', '0.12', '0.13', '0.14', '0.15']
    data_list = []
    for price in prices:
        url = f"https://www.viabtc.com/res/pool/miner?electricity_price={price}"
        r = requests.get(url)
        time.sleep(30)  # Pause between requests to avoid overloading the server
        response = r.json()
        datas = response['data']['miners']
        
        for data in datas:
            try:
                name = data['name']
            except:
                name = ""
            try:
                coin = data['coin']
            except:
                coin = ''
            try:
                hashrate = data['hashrate']+" "+data["hash_unit"]
            except:
                hashrate = ""
            try:
                power = data['power']+" "+data['power_unit']
            except:
                power = ""
            try:
                unit_power = data["unit_power"]+" "+data['power_unit']+"/"+data["hash_unit"]
            except:
                unit_power = ""
            try:
                rev24h = data['unit_output_currency']
            except:
                rev24h = ""
            try:
                electricityFee = data['payout_currency']
            except:
                electricityFee = ""
            try:
                electricRatio = float(data['electricity_fee_percent'])*100
            except:
                electricRatio = ""
            try:
                netProfit24h = data['profit_currency']
            except:
                netProfit24h = ""
            try:
                breakEven = data['shutdown_coin_price']
            except:
                breakEven = ""

                
            temp = {
                "Name":name,
                "Coin":coin,
                "Hash Rate":hashrate,
                "Power":power,
                "Unit Power":unit_power,
                "Rev.24h":rev24h,
                "Electricity Fee":electricityFee,
                "Electricity Ratio":electricRatio,
                "Net Profit 24h":netProfit24h,
                "Break-Even":breakEven,
                "User Electricity Fee": price
            }
            data_list.append(temp)
            print(temp)
            df = pd.DataFrame(data_list)
            

    df = pd.DataFrame(data_list)
    df_sorted = df.sort_values(by=['Coin',"User Electricity Fee"])
    print("Data collected and sorted.")
    connectDatabase(df_sorted)

def connectDatabase(df):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://anshrv17:0D3B2RH0yAlqoSJJ@miners.na2kt.mongodb.net/?retryWrites=true&w=majority&appName=miners",
            tls=True
        )
        db = client['minersInfo']
        collection = db['miners']
        
        records = df.to_dict(orient='records')

        # Loop through each record and update based on Name, Coin, and User Electricity Fee
        for record in records:
            query = {"Name": record['Name'], "Coin": record['Coin'], "User Electricity Fee": record['User Electricity Fee']}
            update = {"$set": record}
            collection.update_one(query, update, upsert=True)  # Use upsert=True to insert new if not found
        
        print("Data updated in MongoDB.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


if __name__=="__main__":
    while True:
        scraper()
        print("Scraper executed, waiting for 5 hours before next run...")
        time.sleep(5 * 60 * 60)  # Sleep for 5 hours (5 hours * 60 minutes * 60 seconds)
