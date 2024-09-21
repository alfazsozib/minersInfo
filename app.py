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
        time.sleep(30)
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
    # df_sorted.to_csv('miners_data.csv', index=False)

    print("Data saved to miners_data.csv and sorted by coin.")
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
        if records:
            collection.insert_many(records)
            print("Inserted records into MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


if __name__=="__main__":
    scraper()

