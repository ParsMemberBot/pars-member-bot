import json
import requests
from bot.main import API_URL

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        # اگر فایل وجود نداشت، برای لیست و دیکشنری بررسی کن
        return [] if file_path.endswith(".json") else {}

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_message(chat_id, text):
    if not text or not chat_id:
        return
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(API_URL + "sendMessage", json=payload)
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)

def send_buttons(chat_id, text, buttons):
    if not text or not chat_id:
        return
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": buttons
        }
    }
    try:
        requests.post(API_URL + "sendMessage", json=payload)
    except Exception as e:
        print("❌ خطا در ارسال دکمه‌ها:", e)
