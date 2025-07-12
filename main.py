from flask import Flask, request
import os
import time
import requests

app = Flask(__name__)

users = {}
ADMIN_ID = "508276871"
TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"

def send_message(chat_id, text, buttons=None):
    print(f"ارسال به {chat_id}: {text}")
    # برای ارسال پیام واقعی با API بله، کد اینجا رو تکمیل کن

def save_data():
    pass  # در صورت نیاز می‌تونی ذخیره‌سازی فایل یا دیتابیس بزاری

def handle_update(data):
    if "message" not in data:
        return

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user_id = str(chat_id)

    if user_id not in users:
        users[user_id] = {"balance": 0}
        save_data()

    if text == "/start":
        send_message(chat_id, "سلام! برای ثبت سفارش از /order استفاده کن.")
    elif text == "/balance":
        send_message(chat_id, f"موجودی شما: {users[user_id]['balance']} تومان")
    elif text == "/order":
        send_message(chat_id, "لطفا تعداد و نوع سفارش را وارد کن.")
    elif text == "/charge":
        send_message(chat_id, "مبلغ مورد نظر را ارسال کنید (حداقل 10000 تومان)")
        users[user_id]["awaiting_charge"] = True
        save_data()
    elif users[user_id].get("awaiting_charge"):
        try:
            amount = int(text)
            users[user_id]["awaiting_charge"] = False
            request_text = f"💳 درخواست افزایش موجودی:\nمبلغ: {amount}\nاز کاربر: {user_id}"
            button = [[{"text": "تایید افزایش", "callback_data": f"approve_{user_id}_{amount}"}]]
            send_message(ADMIN_ID, request_text, buttons=button)
            send_message(chat_id, "درخواست شما ثبت شد و منتظر تایید ادمین است.")
            save_data()
        except:
            send_message(chat_id, "مبلغ نامعتبر است.")
    else:
        send_message(chat_id, "دستور نامعتبر است.")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running."

@app.route(f"/bot{TOKEN}/callback", methods=["POST"])
def callback():
    data = request.json
    if "callback_query" in data:
        query = data["callback_query"]
        data_text = query["data"]
        from_id = str(query["from"]["id"])
        if not data_text.startswith("approve_"):
            return "OK"
        _, user_id, amount = data_text.split("_")
        if from_id != ADMIN_ID:
            return "OK"
        users[user_id]["balance"] += int(amount)
        save_data()
        send_message(user_id, f"✅ مبلغ {amount} تومان به موجودی شما اضافه شد.")
        send_message(from_id, f"✅ تایید شد ({user_id})")
    return "OK"

if __name__ == "__main__":
    last_update_id = 0
    while True:
        try:
            res = requests.get(f"https://bot.bale.ai/bot{TOKEN}/getUpdates?offset={last_update_id + 1}")
            updates = res.json().get("result", [])
            for update in updates:
                last_update_id = update["update_id"]
                handle_update(update)
        except Exception as e:
            print("خطا:", e)

        time.sleep(1)
