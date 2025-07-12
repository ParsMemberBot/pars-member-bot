from flask import Flask, request
import json

app = Flask(__name__)

TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"
ADMIN_ID = "508276871"

users = {}
orders = []

def save_data():
    with open("data/users.json", "w") as f:
        json.dump(users, f)
    with open("data/orders.json", "w") as f:
        json.dump(orders, f)

def load_data():
    global users, orders
    try:
        with open("data/users.json") as f:
            users = json.load(f)
        with open("data/orders.json") as f:
            orders = json.load(f)
    except:
        users, orders = {}, []

load_data()

def send_message(chat_id, text, buttons=None):
    import requests
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}
    headers = {"Content-Type": "application/json"}
    requests.post(f"https://bot.bale.ai/bot{TOKEN}/sendMessage", json=payload, headers=headers)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running."

@app.route(f"/bot{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if not data or "message" not in data:
        return "OK"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user_id = str(chat_id)

    if user_id not in users:
        users[user_id] = {"balance": 0}
        save_data()

    if text == "/start":
        send_message(chat_id, "سلام! 👋\nبرای ثبت سفارش از /order استفاده کن.\nبرای افزایش موجودی از /charge استفاده کن.\nبرای مشاهده موجودی از /balance استفاده کن.")
    elif text == "/balance":
        send_message(chat_id, f"موجودی شما: {users[user_id]['balance']} تومان")
    elif text == "/order":
        send_message(chat_id, "لطفاً سرویس، تعداد، و لینک رو وارد کن. مثلا:\n\nسرویس ممبر واقعی\nتعداد: 1000\nلینک: https://t.me/test")
    elif text == "/charge":
        send_message(chat_id, "مبلغ مورد نظرت رو برای شارژ بفرست (مثلا 10000).")
        users[user_id]["awaiting_charge"] = True
        save_data()
    elif users[user_id].get("awaiting_charge"):
        try:
            amount = int(text)
            users[user_id]["awaiting_charge"] = False
            request_text = f"📥 درخواست افزایش موجودی:\nمبلغ: {amount} تومان\nاز کاربر: {chat_id}"
            button = [[{"text": "✅ تایید افزایش", "callback_data": f"approve_{chat_id}_{amount}"}]]
            send_message(ADMIN_ID, request_text, buttons=button)
            send_message(chat_id, "درخواست شما ثبت شد و منتظر تایید ادمین است.")
            save_data()
        except:
            send_message(chat_id, "مبلغ نامعتبر است.")
    return "OK"

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
        send_message(from_id, f"✅ شارژ شد ({user_id}) موجودی کاربر.")
    return "OK"
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
