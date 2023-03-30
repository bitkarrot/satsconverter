import requests
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from locale import atof, setlocale, LC_NUMERIC

# import uvicorn

def get_block_height():
    url = "https://api.blockchair.com/bitcoin/stats"
    res = requests.get(url)
    data = res.json()
    height = data['data']['best_block_height']
    return height


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


title = "sats converter"
description = "simple web app to convert fiat to btc"

app = FastAPI(
    title=title,
    description=description,
    version="0.0.1 alpha",
    contact={
        "name": "bitkarrot",
        "url": "http://github.com/bitkarrot",
    },
    license_info={
        "name": "MIT License",
        "url": "https://mit-license.org/",
    },
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory='templates/')


@app.get("/")
def initial_page(request: Request):
    time, usdrate = coindesk_btc_fiat('USD')
    btcusd = "%.2f" % usdrate
    time, rate = coindesk_btc_fiat('HKD')
    btchkd = "%.2f" % rate
    moscowtime = int(100000000/float(btcusd))
    height = get_block_height()
    return templates.TemplateResponse("index.html",
                                      context={
                                          'request': request,
                                          'title': "Sats Converter",
                                          'usdprice': btcusd,
                                          'fiatprice': btchkd,
                                          'moscow': moscowtime,
                                          'blockheight': height,
                                          'lastupdated': time})


# @app.route('/', methods=('POST'))
# def convert_pricing():
#     if request.method == 'POST':
#          fiat_amt = request.form['fiatamt']
#          sats_amt = request.form['satsamt']
#     return render_template("index.html", title="Converted",
#                            fiatprice=fiat_amt, btcprice=sats_amt)
