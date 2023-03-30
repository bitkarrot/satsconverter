# https://www.coingecko.com/en/api/documentation
import requests

base_url = "https://api.coingecko.com/api/v3"

def ping(): 
    response = requests.get(base_url + "/ping")
    data = response.json()
    return data


# if __name__ == "__main__":
#     print(ping())