import requests
from bot.config import TOKEN

API_URL = f"https://tapi.bale.ai/bot{TOKEN}"

def send_message(chat_id, text, keyboard=None, inline=False):
    # بررسی اینکه متن پیام خالی نباشد
    if not text:
        print("⛔ تلاش برای ارسال پیام بدون متن. ارسال پیام لغو شد.")
        return

    url = f"{API_URL}/sendMessage"
    data = {
        "chatId": chat_id,
        "message": text
    }
    if keyboard:
        if inline:
            data["replyMarkup"] = {
                "inlineKeyboard": keyboard
            }
        else:
            data["replyMarkup"] = {
                "keyboard": keyboard,
                "resizeKeyboard": True
            }
    try:
        res = requests.post(url, json=data)
        if res.status_code != 200:
            print("❌ خطا در ارسال پیام:", res.text)
    except Exception as e:
        print(f"Error sending message: {e}")

def load_data(path):
    import json, os
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(path, data):
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def is_user_admin(user_id):
    from bot.config import OWNER_ID
    admins = load_data("data/admins.json").get("admins", [])
    return user_id == OWNER_ID or user_id in admins

def format_price(price):
    return f"{price:,} تومان"

def has_joined_required_channels(user_info):
    return True  # در صورت نیاز عضویت اجباری رو اینجا کنترل کن
