import requests
import time

TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}"

def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"offset": offset}
    try:
        response = requests.get(url, params=params)
        return response.json()["result"]
    except Exception as e:
        print("❌ خطا در دریافت پیام‌ها:", e)
        return []

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)

def main():
    print("✅ ربات بله روی Render با API جدید شروع به کار کرد...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            try:
                chat_id = update["message"]["chat"]["id"]
                user_text = update["message"].get("text", "")
                print(f"📩 پیام جدید: {user_text}")
                send_message(chat_id, "سلام از ربات بله!")
                offset = update["update_id"] + 1
            except Exception as e:
                print("⚠️ خطا در پردازش پیام:", e)
        time.sleep(1)

if __name__ == "__main__":
    main()
