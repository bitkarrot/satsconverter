import requests
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated

from locale import atof, setlocale, LC_NUMERIC
import logging

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
async def initial_page(request: Request):
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
                                          'btcprice': btcusd,
                                          'fiat': btchkd,
                                          'satsamt': 1.0,
                                          'moscow': moscowtime,
                                          'blockheight': height,
                                          'lastupdated': time})


@app.post("/")
async def convert(request: Request, fiat: float = Form(...),  # trunk-ignore(ruff/B008)
                  satsamt: float = Form(...),   # trunk-ignore(ruff/B008)
                  fiatselect: str = Form(...),  # trunk-ignore(ruff/B008)
                  satselect: str = Form(...)):  # trunk-ignore(ruff/B008)
    try:
        data =  {'fiat': fiat,
                'sats': satsamt,
                'fiatselect': fiatselect,
                'satselect': satselect}
        print(data)
        return templates.TemplateResponse("index.html",
                                      context={
                                          'request': request,
                                          'title': "Converter!"})

    except Exception as e:
        logging.error(e)
