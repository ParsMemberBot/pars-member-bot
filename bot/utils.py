import json
import requests
from bot.config import TOKEN

API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

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
        print("⚠️ پیام خالی یا chat_id نامعتبر بود، ارسال نشد.")
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
        print("⚠️ متن یا chat_id برای دکمه خالی بود.")
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

def edit_message(chat_id, message_id, text):
    if not text or not chat_id or not message_id:
        print("⚠️ داده ناقص برای ویرایش پیام.")
        return
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }
    try:
        requests.post(API_URL + "editMessageText", json=payload)
    except Exception as e:
        print("❌ خطا در ویرایش پیام:", e)
