from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ENV KEYS
FLW_PUBLIC_KEY = os.getenv("FLUTTERWAVE_PUBLIC_KEY")
FLW_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY")
NOWNODES_API_KEY = os.getenv("NOWNODES_API_KEY")

# WALLET ADDRESSES (REPLACE WITH YOURS IF NEEDED)
BTC_WALLET = "bc1qh8es4m9mjua5w08qv00"
USDT_WALLET = "UQCtCm584SIWPddaOQ9ec8MULk2Aqi5ucw2s073DzNtQQc6L"
ETH_WALLET = "0xf22566f4a5b70437e33f8c846e3780f4609e2abe"
XRP_WALLET = "rf9nJMNU3Y2D8EkeDG4Z4f9qUPhThdrsGk"
SOL_WALLET = "5msvCNwA3boDLKrgBEA8MPTnFq4bfeEqTttyEnr2nnsM"
BCH_WALLET = "bitcoincash:qzk5keejgnc0urhqtrq3lk8xrus6nef5gvxh4476qa"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("payment.html", {
        "request": request,
        "flw_key": FLW_PUBLIC_KEY,
        "btc_wallet": BTC_WALLET,
        "usdt_wallet": USDT_WALLET,
        "eth_wallet": ETH_WALLET,
        "xrp_wallet": XRP_WALLET,
        "sol_wallet": SOL_WALLET,
        "bch_wallet": BCH_WALLET,
    })

@app.post("/process")
async def process_payment(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    amount: float = Form(...),
    currency: str = Form(...)
):
    # You can handle logging or API communication here
    return RedirectResponse("/thank-you", status_code=302)

@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thank_you.html", {"request": request})

@app.get("/btc-address-check")
async def check_btc_balance():
    url = f"https://btcbook.nownodes.io/api/v2/address/{BTC_WALLET}"
    headers = {"api-key": NOWNODES_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()
