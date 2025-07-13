import json
import requests

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_message(chat_id, text, reply_markup=None):
    from main import API_URL
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(API_URL + "sendMessage", data=data)

def kick_user(chat_id, user_id):
    from main import API_URL
    data = {"chat_id": chat_id, "user_id": user_id}
    requests.post(API_URL + "kickChatMember", data=data)
