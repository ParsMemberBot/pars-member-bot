import requests
import json
import os

TOKEN = "1010361809:u9favCTJqt5zgmHkMAhO2sBJYqMUcsMkCCiycx1D"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

def send_message(chat_id, text, reply_markup=None):
    if not text:
        print("❗ پیام خالی بود و ارسال نشد.")
        return
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    try:
        res = requests.post(API_URL + "sendMessage", json=payload)
        print("📤 پاسخ بله‌سا:", res.text)
    except Exception as e:
        print("❌ خطا در ارسال:", e)


def load_data(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
