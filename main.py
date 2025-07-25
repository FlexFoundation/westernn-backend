from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 🔐 Your crypto wallet addresses
BTC_WALLET = "bc1qh8es4m9mjua5w08qv00"
USDT_WALLET = "TE6bcewMeHxn8USQ65baJh4ynx8Qw5dvop"

# 🔐 Load Flutterwave secret key from Render environment variable
FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")

# 🧾 Sample HTML payment form page
@app.get("/pay", response_class=HTMLResponse)
async def get_payment_form(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

# ✅ Webhook to receive transaction events from Flutterwave
@app.post("/webhook")
async def flutterwave_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    # Flutterwave verification
    event_type = payload.get("event")
    if event_type == "charge.completed":
        data = payload.get("data", {})
        status = data.get("status")
        amount = data.get("amount")
        currency = data.get("currency")
        customer_wallet = data.get("meta", {}).get("wallet")  # assuming user input

        if status == "successful":
            print(f"✅ Payment received: {amount} {currency}")

            # Simulate crypto send in background
            background_tasks.add_task(send_crypto, currency, amount, customer_wallet)

    return {"status": "ok"}

# 🔁 Function to simulate sending crypto to user wallet
def send_crypto(currency: str, amount: float, wallet_address: Optional[str]):
    if not wallet_address:
        print("❌ No wallet address provided.")
        return

    # Simulated: Convert fiat to crypto using your own rate
    crypto_amount = amount / 100  # Just a fake conversion logic
    print(f"💸 Sending {crypto_amount} {currency} worth to {wallet_address}")
    # Replace with actual crypto send logic here using API or RPC
