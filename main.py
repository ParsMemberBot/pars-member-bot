import os
import json
import time
import requests
from bot.utils import load_data, save_data
from bot.commands import handle_start, handle_menu
from bot.store import handle_store
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.fun import handle_fun_commands

# ✅ توکن واقعی ربات شما
TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

OFFSET_FILE = "data/offset.txt"

def get_updates(offset=None):
    try:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        res = requests.get(API_URL + "getUpdates", params=params)
        return res.json()["result"]
    except Exception as e:
        print("خطا در دریافت آپدیت‌ها:", e)
        return []

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(API_URL + "sendMessage", data=data)

def handle_support(chat_id):
    text = "جهت ارتباط با پشتیبانی به آیدی زیر پیام دهید:\n@CyrusParsy"
    send_message(chat_id, text)

def handle_profile(chat_id, user_id):
    users = load_data("data/users.json")
    user = users.get(str(user_id), {"balance": 0, "orders": []})
    text = f"💼 حساب کاربری شما:\n\n👤 آیدی عددی: {user_id}\n💰 موجودی: {user['balance']} تومان\n🛒 تعداد سفارش‌ها: {len(user['orders'])}"
    send_message(chat_id, text)

def handle_update(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    text = msg.get("text", "")

    if text.startswith("/start"):
        handle_start(chat_id, user_id)
    elif text in ["منو", "بازگشت"]:
        handle_menu(chat_id, user_id)
    elif text in ["فروشگاه", "سفارش"]:
        handle_store(chat_id, user_id)
    elif text in ["پنل مدیریت", "/admin"]:
        handle_admin_panel(chat_id, user_id)
    elif text in ["جوک", "فال"] or text.startswith("/ai") or text.startswith("هوش مصنوعی") or text.startswith("ربات"):
        handle_fun_commands(msg)
    elif text.startswith("پشتیبانی") or "پشتیبانی" in text:
        handle_support(chat_id)
    elif text.startswith("حساب کاربری") or "حساب" in text:
        handle_profile(chat_id, user_id)
    else:
        handle_group_message(msg)

def main():
    print("🤖 ربات روشن است.")
    offset = 0
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE) as f:
            try:
                offset = int(f.read())
            except Exception as e:
                print("خطا در خواندن offset.txt:", e)
                offset = 0

    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                handle_update(update)
                offset = update["update_id"] + 1
            with open(OFFSET_FILE, "w") as f:
                f.write(str(offset))
        time.sleep(1)

if __name__ == "__main__":
    main()
