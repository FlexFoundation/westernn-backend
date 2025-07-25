from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import httpx
import asyncio
import os

app = FastAPI()

# 🧠 Wallet addresses
BTC_WALLET = "bc1qh8es4m9mjua5w08qv00"
USDT_WALLET = "UQCtCm584SIWPddaOQ9ec8MULk2Aqi5ucw2s073DzNtQQc6L"

# 🌐 Templates folder
templates = Jinja2Templates(directory="templates")

# 📄 Home page – form to choose payment type
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

# 💳 Handle card payments via Flutterwave
@app.post("/pay-card")
async def pay_card(
    request: Request,
    amount: str = Form(...),
    email: str = Form(...)
):
    flutterwave_pub_key = os.getenv("FLW_PUBLIC_KEY", "FLWPUBK_TEST-xxxxxxxxxxxxxxxxxxxxxx-X")
    
    # Flutterwave inline payment link
    redirect_url = f"https://checkout.flutterwave.com/v3/hosted/pay?public_key={flutterwave_pub_key}&tx_ref=TX-{email}&amount={amount}&currency=USD&customer[email]={email}&redirect_url=https://yourdomain.com/success"

    return RedirectResponse(redirect_url)

# 🌍 Fetch live BTC rate (optional)
@app.get("/btc-rate")
async def get_btc_rate():
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        rate = res.json().get("bitcoin", {}).get("usd", None)
        return {"btc_usd": rate}
