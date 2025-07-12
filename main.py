import time
import requests

TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"
URL = f"https://bot.bale.ai/bot{TOKEN}"

def get_updates(offset=None):
    try:
        params = {"offset": offset, "timeout": 10}
        response = requests.get(f"{URL}/getUpdates", params=params)
        return response.json()
    except:
        return {}

def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(f"{URL}/sendMessage", json=payload)

def main():
    print("✅ ربات تستی فعال شد...")
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        for update in updates.get("result", []):
            last_update_id = update["update_id"] + 1
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")

            # پاسخ به همه پیام‌ها
            send_message(chat_id, "سلام")

        time.sleep(1)

if __name__ == "__main__":
    main()
