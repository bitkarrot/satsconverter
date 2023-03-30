# https://www.coingecko.com/en/api/documentation
import requests

base_url = "https://api.coingecko.com/api/v3"

def ping(): 
    response = requests.get(base_url + "/ping")
    data = response.json()
    return data

def getBTCvsFiat(fiat):
    response = requests.get(base_url + "/simple/price?ids=bitcoin&vs_currencies=" + fiat)
    data = response.json()
    return data

def getBTCTicker():
    res = requests.get(base_url + "/coins/bitcoin/tickers")
    data = res.json()
    return data

if __name__ == "__main__":
   # print(getBTCTicker())
   print(getBTCvsFiat("USD"))
#     print(ping())
