import os

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from datetime import datetime

load_dotenv()

TELEGRAM_BOT_API = os.getenv('BOT_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
app = FastAPI()
ANSWERS = {}


@app.get("/ans")
async def get_ans():
    global ANSWERS
    return ANSWERS


@app.post("/upl")
async def post_upl(m: str):
    global ANSWERS
    ANSWERS[datetime.now().strftime("%H:%M:%S")] = m
    return "OK"


@app.get("/msg")
async def post_msg(m: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': m
    }
    response = requests.post(url, json=payload)
    return response.json()['ok']


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
