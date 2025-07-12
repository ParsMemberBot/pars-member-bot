from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "توکن شما اینجاست"

def send_message(chat_id, text):
    url = f"https://bot.bale.ai/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    print("📥 دریافت شد:", data)
    try:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(chat_id, "سلام! به ربات بله خوش اومدی.")
        else:
            send_message(chat_id, f"شما گفتی: {text}")
    except Exception as e:
        print("❌ خطا:", e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
