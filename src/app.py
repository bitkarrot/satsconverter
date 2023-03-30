import requests
from flask import Flask, render_template
from locale import atof, setlocale, LC_NUMERIC

def coindesk_btc_fiat(symbol):
    # batch the requests together via asyncio or multiprocessing
    setlocale(LC_NUMERIC, '')
    url = f'https://api.coindesk.com/v1/bpi/currentprice/{symbol}.json'
    response = requests.get(url)
    ticker = response.json()
    time = ticker["time"]['updated']
    rate = ticker['bpi'][symbol]['rate']
    r = atof(rate)
    return time, r


app = Flask(__name__)

@app.route('/')
def home():
    time, usdrate = coindesk_btc_fiat('USD')
    btcusd = "%.2f" % usdrate
    time, rate = coindesk_btc_fiat('HKD')
    btchkd = "%.2f" % rate
    moscowtime = int(100000000/float(btcusd))
    return render_template("index.html", title="Sats Converter", usdprice=btcusd, hkdprice=btchkd, moscow=moscowtime, lastupdated=time)


@app.route('/about')
def about():
    return 'About this app'