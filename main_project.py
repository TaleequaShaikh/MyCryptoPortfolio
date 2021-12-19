import requests # this module helps us to fetch/get data and send http request
import json # this module helps to parse data
api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=6&convert=USD&CMC_PRO_API_KEY=8092d883-9a5b-4ef6-886c-b9c10db")
# api_request is a variable that stores api link ka data
api = json.loads(api_request.content) # helps to deliver the content of api_request

print("--------------")
print("--------------")

coins = [
    { "symbol" : "BTC",
       "Num_of_coins_owned" : 1,
       "price_per_coin" : 31945.41
    },
    { "symbol" : "ETH",
       "Num_of_coins_owned" : 2,
       "price_per_coin" : 1948.36
    },
    { "symbol" : "BNB",
       "Num_of_coins_owned" : 1,
       "price_per_coin" : 321.35
    }
]

total_pl = 0

for i in range(0,6):
    for coin in coins:
        if api["data"][i]["symbol"] == coin[1]:
            total_paid = coin[2] * coin["price_per_coin" ]
            current_value = api["data"][i]["quote"]["USD"]["price"] * coin[2]
            pl_percoin =  api["data"][i]["quote"]["USD"]["price"] - coin[3] 
            total_pl_coin = pl_percoin * coin[2]
            
            total_pl = total_pl + total_pl_coin

            print(api["data"][i]["name"] + " _ " + api["data"][i]["symbol"])
            print("Price per coin - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
            print("Total Amount Paid", "${0:.2f}".format(total_paid))
            print("Current value of Coin","${0:.2f}".format(current_value))
            print("Profit/Loss per Coin", "${0:.2f}".format(pl_percoin))
            print("Total Profit/Loss With Coin","${0:.2f}".format(total_pl_coin))
            print("--------------")        

print("Total P/L For Portfolio:", "${0:.2f}".format(total_pl))
