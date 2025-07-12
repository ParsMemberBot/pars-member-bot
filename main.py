from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route('/', methods=["POST"])
def webhook():
    data = request.json
    try:
        chat_id = data["message"]["chat"]["id"]
        # هر پیامی بده، جواب سلام بده
        send_message(chat_id, "سلام 👋")
    except Exception as e:
        print("❌ خطا:", e)
    return "OK", 200

def send_message(chat_id, text):
    TOKEN = "توکن_ربات_شما"
    url = f"https://bot.bale.ai/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
