import requests
import json

TOKEN = "1010361809:u9favCTJqt5zgmHkMAhO2sBJYqMUcsMkCCiycx1D"
API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

def send_message(chat_id, text, reply_markup=None):
    if not text:  # جلوگیری از ارور text is empty
        print("❗پیام بدون متن ارسال نشد.")
        return

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    try:
        res = requests.post(API_URL + "sendMessage", json=payload)
        print("📤 پیام ارسال شد:", res.text)
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)
