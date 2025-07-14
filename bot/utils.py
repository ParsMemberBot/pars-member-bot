import requests
import json

# توکن ربات توی این آدرس API جایگذاری شده
API_URL = "https://tapi.bale.ai/bot1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27/"

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(API_URL + "sendMessage", data=data)

def kick_user(chat_id, user_id):
    data = {
        "chat_id": chat_id,
        "user_id": user_id
    }
    requests.post(API_URL + "kickChatMember", data=data)

def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
