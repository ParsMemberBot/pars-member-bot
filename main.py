from keep_alive import keep_alive
import requests
import time

keep_alive()  # روشن نگه‌داشتن ربات در Replit

TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"
ADMIN_ID = "508276871"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}"

users = {}

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
    print("✅ ربات بله روشن شد...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            try:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                print(f"📩 پیام از {chat_id}: {text}")

                # اولین ثبت کاربر
                if str(chat_id) not in users:
                    users[str(chat_id)] = {"balance": 0}

                if text == "/start":
                    send_message(chat_id, "سلام! به ربات خوش آمدید.\n\nدستورها:\n/balance → موجودی\n/charge → افزایش موجودی\n/order → ثبت سفارش")

                elif text == "/balance":
                    send_message(chat_id, f"موجودی شما: {users[str(chat_id)]['balance']} تومان")

                elif text == "/charge":
                    send_message(chat_id, "مبلغ مورد نظر برای شارژ را وارد کنید:")
                    users[str(chat_id)]["awaiting_charge"] = True

                elif users[str(chat_id)].get("awaiting_charge"):
                    try:
                        amount = int(text)
                        users[str(chat_id)]["balance"] += amount
                        users[str(chat_id)]["awaiting_charge"] = False
                        send_message(chat_id, f"✅ {amount} تومان به موجودی شما اضافه شد.")
                        # پیام به ادمین
                        send_message(ADMIN_ID, f"🔔 {chat_id} موجودی را {amount} تومان افزایش داد.")
                    except:
                        send_message(chat_id, "❌ مبلغ معتبر نیست. لطفاً عدد وارد کنید.")

                elif text == "/order":
                    send_message(chat_id, "فعلاً فروشگاه فعال نیست. به زودی اضافه می‌شود.")

                else:
                    send_message(chat_id, "❓ دستور نامعتبر است.")

                offset = update["update_id"] + 1

            except Exception as e:
                print("⚠️ خطا در پردازش پیام:", e)
        time.sleep(1)

if __name__ == "__main__":
    main()
