import time
import requests

TOKEN = "توکن‌ ربات‌تو‌ اینجا بذار"
BASE_URL = f"https://bot.bale.ai/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def main():
    last_update_id = None
    print("🤖 ربات سلف بله شروع به کار کرد ...")
    while True:
        updates = get_updates(last_update_id)
        for update in updates.get("result", []):
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            if chat_id and text:
                send_message(chat_id, "سلام 👋")

            last_update_id = update["update_id"] + 1

        time.sleep(2)  # هر ۲ ثانیه چک کنه

if __name__ == "__main__":
    main()
