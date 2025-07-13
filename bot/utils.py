import json
import os
import requests

def send_message(chat_id, text, reply_markup=None):
    from main import API_URL
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(API_URL + "sendMessage", data=data)
    except:
        pass

def load_data(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def chatgpt_response(prompt):
    try:
        url = f"https://li.linto.ir/api/bingchat/?text={prompt}"
        res = requests.get(url, timeout=15)
        data = res.json()
        return data.get("result", {}).get("text", "❌ پاسخی از هوش مصنوعی دریافت نشد.")
    except Exception as e:
        return f"⚠️ خطا در ارتباط با هوش مصنوعی: {e}"
