from fastapi import FastAPI, Request, Form from fastapi.responses import HTMLResponse, RedirectResponse from pydantic import BaseModel import datetime import json import httpx

app = FastAPI()

WALLET ADDRESSES (Replace with yours)

BTC_WALLET = "bc1qh8es4m9mjua5w08qv00" USDT_WALLET = "UQCtCm584SIWPddaOQ9ec8MULk2Aqi5ucw2s073DzNtQQc6L" ETH_WALLET = "0xf22566f4a5b70437e33f8c846e3780f4609e2abe" XRP_WALLET = "rf9nJMNU3Y2D8EkeDG4Z4f9qUPhThdrsGk" SOL_WALLET = "5msvCNwA3boDLKrgBEA8MPTnFq4bfeEqTttyEnr2nnsM" BCH_WALLET = "bitcoincash:qzk5keejgnc0urhqtrq3lk8xrus6nef5gvxh4476qa"

@app.get("/") def read_root(): return {"message": "Welcome to Westernn - Your crypto gateway is live!"}

@app.post("/webhook") async def handle_webhook(request: Request): payload = await request.json() event_type = payload.get("event")

if event_type == "charge.completed":
    data = payload.get("data", {})
    tx_ref = data.get("tx_ref")
    amount = data.get("amount")
    currency = data.get("currency")
    email = data.get("customer", {}).get("email")
    meta = data.get("meta", {})
    crypto_type = meta.get("crypto")  # Example: BTC, USDT, etc.
    wallet_address = meta.get("wallet")  # User's provided wallet address

    if crypto_type and wallet_address:
        # Simulate crypto conversion + sending
        print(f"Received {amount} {currency} from {email}, converting to {crypto_type} and sending to {wallet_address}.")
        # You can add your own rate logic or call API to convert

return {"status": "success"}

@app.get("/payment", response_class=HTMLResponse) def payment_page(): return """ <html> <head><title>Westernn Payment</title></head> <body> <h2>Pay with Card</h2> <form action="https://checkout.flutterwave.com/v3/hosted/pay" method="GET"> <button type="submit">Pay Now</button> </form> <br/> <h2>Pay with Crypto</h2> <ul> <li>BTC: bc1qh8es4m9mjua5w08qv00</li> <li>USDT (TRC20): UQCtCm584SIWPddaOQ9ec8MULk2Aqi5ucw2s073DzNtQQc6L</li> <li>ETH: 0xf22566f4a5b70437e33f8c846e3780f4609e2abe</li> <li>XRP: rf9nJMNU3Y2D8EkeDG4Z4f9qUPhThdrsGk</li> <li>SOL: 5msvCNwA3boDLKrgBEA8MPTnFq4bfeEqTttyEnr2nnsM</li> <li>BCH: bitcoincash:qzk5keejgnc0urhqtrq3lk8xrus6nef5gvxh4476qa</li> </ul> </body> </html> """

@app.get("/thank-you") def thank_you(): return {"message": "Payment successful! Crypto is on the way."}

You can expand this with logging, conversions, etc.

