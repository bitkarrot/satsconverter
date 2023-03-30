from flask import Flask, render_template
from coindesk import coindesk_btc_fiat

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