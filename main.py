from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Wallets ---
BTC_WALLET = os.getenv("BTC_WALLET", "your-btc-wallet")
USDT_WALLET = os.getenv("USDT_WALLET", "your-usdt-wallet")
ETH_WALLET = os.getenv("ETH_WALLET", "your-eth-wallet")
SOL_WALLET = os.getenv("SOL_WALLET", "your-sol-wallet")
XRP_WALLET = os.getenv("XRP_WALLET", "your-xrp-wallet")
BCH_WALLET = os.getenv("BCH_WALLET", "your-bch-wallet")

@app.get("/", response_class=HTMLResponse)
def payment_page(request: Request):
    return templates.TemplateResponse("payment.html", {
        "request": request,
        "btc_wallet": BTC_WALLET,
        "usdt_wallet": USDT_WALLET,
        "eth_wallet": ETH_WALLET,
        "sol_wallet": SOL_WALLET,
        "xrp_wallet": XRP_WALLET,
        "bch_wallet": BCH_WALLET
    })

@app.post("/thankyou", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thank_you.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
