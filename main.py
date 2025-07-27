from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uuid

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Wallet addresses
BTC = os.getenv("BTC_WALLET")
USDT = os.getenv("USDT_WALLET")
ETH = os.getenv("ETH_WALLET")
SOL = os.getenv("SOL_WALLET")
XRP = os.getenv("XRP_WALLET")
BCH = os.getenv("BCH_WALLET")

# Flutterwave API
FLW_PUBLIC_KEY = os.getenv("FLW_PUBLIC_KEY")

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("payment.html", {
        "request": request,
        "flw_public_key": FLW_PUBLIC_KEY
    })

@app.post("/pay", response_class=RedirectResponse)
async def process_payment(amount: str = Form(...), email: str = Form(...)):
    tx_ref = str(uuid.uuid4())
    flutterwave_url = f"https://flutterwave.com/pay/{tx_ref}"
    return RedirectResponse(url=flutterwave_url, status_code=303)

@app.get("/thankyou", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thankyou.html", {
        "request": request,
        "btc": BTC,
        "usdt": USDT,
        "eth": ETH,
        "sol": SOL,
        "xrp": XRP,
        "bch": BCH,
    })
