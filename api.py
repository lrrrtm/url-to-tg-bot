import os

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
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
    ANSWERS[f"{datetime.now().strftime('%H:%M:%S')} <-"] = m
    return "OK"


@app.get("/msg")
async def post_msg(m: str):
    global ANSWERS
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': m
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        ANSWERS[f"{datetime.now().strftime('%H:%M:%S')} OK ->"] = m
    else:
        ANSWERS[f"{datetime.now().strftime('%H:%M:%S')} ER ->"] = m
    return RedirectResponse(url="/ans")

# Определение корневой страницы с формой загрузки файла
@app.get("/pdf", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <body>
            <form action="/send-files/" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple>
                <input type="submit" value="Отправить">
            </form>
        </body>
    </html>
    """




@app.post("/send-files")
async def send_files(files: list[UploadFile] = File(...)):
    responses = []
    for file in files:
        contents = await file.read()
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendDocument"
        files_data = {"document": (file.filename, contents)}
        data = {"chat_id": CHAT_ID}
        response = requests.post(url, files=files_data, data=data)
        responses.append(response.json().get('ok'))
    return {"responses": responses}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
