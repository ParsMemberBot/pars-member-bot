import json
import requests
from bot.config import TOKEN

API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [] if file_path.endswith(".json") else {}


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text, reply_markup=None):
    if not text or not chat_id:
        print("⚠️ پیام یا chat_id خالی است.")
        return
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        requests.post(API_URL + "sendMessage", json=payload)
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)


def send_buttons(chat_id, text, buttons):
    if not text or not chat_id:
        print("⚠️ متن یا chat_id برای دکمه خالی است.")
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


def edit_message(chat_id, message_id, text, buttons=None):
    if not chat_id or not message_id:
        print("⚠️ chat_id یا message_id نامعتبر است.")
        return
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }
    if buttons:
        payload["reply_markup"] = {
            "inline_keyboard": buttons
        }
    try:
        requests.post(API_URL + "editMessageText", json=payload)
    except Exception as e:
        print("❌ خطا در ویرایش پیام:", e)


def send_menu(chat_id):
    text = "به منوی اصلی ربات خوش آمدید 🌟"
    buttons = [
        [{"text": "💰 افزایش موجودی"}],
        [{"text": "🛒 ثبت سفارش"}, {"text": "📩 حساب کاربری"}],
        [{"text": "🔧 پنل مدیریت"}, {"text": "ℹ️ پشتیبانی"}],
    ]
    reply_markup = {
        "keyboard": buttons,
        "resize_keyboard": True
    }
    send_message(chat_id, text, reply_markup=reply_markup)


def user_link(user):
    if user.get("username"):
        return f"@{user['username']}"
    return f"[{user.get('first_name', 'کاربر') or 'کاربر'}](tg://user?id={user['id']})"
