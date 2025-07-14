import os
import time
import requests
from bot.utils import load_data, save_data
from bot.commands import handle_command

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
    print("📥 پیام دریافتی:", msg)
    try:
        handle_command(msg, is_group)
    except Exception as e:
        print("❌ خطا در پردازش پیام:", e)

def main():
    print("✅ ربات با موفقیت روشن شد.")
    offset = 0

    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as f:
            try:
                offset = int(f.read().strip())
            except:
                offset = 0

    while True:
        updates = get_updates(offset)
        for update in updates:
            handle_update(update)

            # ⛳️ ذخیره offset با استفاده از update_id
            update_id = update.get("update_id")
            if update_id:
                offset = update_id + 1
                with open(OFFSET_FILE, "w") as f:
                    f.write(str(offset))
        time.sleep(1)

if __name__ == "__main__":
    main()
