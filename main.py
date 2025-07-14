import os
import json
import time
import requests
from bot.utils import load_data, save_data
from bot.commands import handle_command  # تغییر مهم: استفاده از تابع واحد
from bot.fun import handle_fun_commands  # اگر خواستی جداگانه هم بمونه

# توکن واقعی ربات شما
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

def handle_update(update):
    if "message" not in update:
        return
    msg = update["message"]
    is_group = msg["chat"]["type"] in ["group", "supergroup"]
    handle_command(msg, is_group)

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
