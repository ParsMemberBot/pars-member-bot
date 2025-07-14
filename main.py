import os
import json
import time
import requests
from bot.utils import load_data, save_data
from bot.commands import handle_command  # ✅ هدایت تمام دستورات به این تابع

# 🔐 توکن واقعی ربات شما
TOKEN = "1010361809:u9favCTJqt5zgmHkMAhO2sBJYqMUcsMkCCiycx1D"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

OFFSET_FILE = "data/offset.txt"

def get_updates(offset=None):
    try:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        res = requests.get(API_URL + "getUpdates", params=params)
        return res.json().get("result", [])
    except Exception as e:
        print("❌ خطا در دریافت آپدیت‌ها:", e)
        return []

def handle_update(update):
    if "message" not in update:
        return
    msg = update["message"]
    is_group = msg.get("chat", {}).get("type") in ["group", "supergroup"]
    handle_command(msg, is_group)

def main():
    print("✅ ربات با موفقیت روشن شد.")
    offset = 0

    # بازیابی offset از فایل
    if os.path.exists(OFFSET_FILE):
        try:
            with open(OFFSET_FILE) as f:
                offset = int(f.read().strip())
        except Exception as e:
            print("⚠️ خطا در خواندن فایل offset:", e)

    # حلقه اصلی دریافت پیام‌ها
    while True:
        updates = get_updates(offset)
        for update in updates:
            handle_update(update)
            offset = update["update_id"] + 1
        with open(OFFSET_FILE, "w") as f:
            f.write(str(offset))
        time.sleep(1)

if __name__ == "__main__":
    main()
