from flask import Flask, request
import os

app = Flask(__name__)

users = {}
ADMIN_ID = "123456789"  # آیدی عددی ادمین را اینجا بذار
TOKEN = "توکن_ربات_بله"

def send_message(chat_id, text, buttons=None):
    print(f"ارسال به {chat_id}: {text}")

def save_data():
    pass

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
        send_message(chat_id, "سلام! برای ثبت سفارش از /order استفاده کن.")
    elif text == "/balance":
        send_message(chat_id, f"موجودی شما: {users[user_id]['balance']} تومان")
    elif text == "/order":
        send_message(chat_id, "لینک و تعداد رو وارد کن...")
    elif text == "/charge":
        send_message(chat_id, "مبلغ مورد نظر را ارسال کنید (مثلا 10000)")
        users[user_id]["awaiting_charge"] = True
        save_data()
    elif users[user_id].get("awaiting_charge"):
        try:
            amount = int(text)
            users[user_id]["awaiting_charge"] = False
            request_text = f"📥 درخواست افزایش موجودی:\nمبلغ: {amount}\nاز کاربر: {user_id}"
            button = [[{"text": "✅ تأیید افزایش", "callback_data": f"approve_{user_id}_{amount}"}]]
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
        send_message(from_id, f"✅ کاربر {user_id} شارژ شد.")
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
