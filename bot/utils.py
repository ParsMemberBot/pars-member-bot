import json
import requests

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"خطا در ذخیره‌سازی {filename}:", e)

def send_message(chat_id, text, reply_markup=None):
    try:
        from main import API_URL
        data = {"chat_id": chat_id, "text": text}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        requests.post(API_URL + "sendMessage", data=data)
    except Exception as e:
        print("خطا در ارسال پیام:", e)
