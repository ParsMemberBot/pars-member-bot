import json
import requests

# ارسال پیام متنی ساده
def send_message(chat_id, text, reply_markup=None):
    from bot.main import API_URL
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(API_URL + "sendMessage", data=data)

# اخراج کاربر از گروه
def kick_user(chat_id, user_id):
    from bot.main import API_URL
    data = {
        "chat_id": chat_id,
        "user_id": user_id
    }
    requests.post(API_URL + "kickChatMember", data=data)

# درخواست از API چت‌جی‌پی‌تی (از API آماده استفاده می‌کنیم)
def chatgpt_response(prompt):
    try:
        url = f"https://li.linto.ir/api/bingchat/?text={prompt}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("result", {}).get("text", "❌ پاسخ نامشخص از هوش مصنوعی دریافت شد.")
        else:
            return "❌ خطا در ارتباط با API هوش مصنوعی."
    except:
        return "❌ ارتباط با سرور هوش مصنوعی برقرار نشد."

# لود داده‌ها از فایل
def load_data(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

# ذخیره داده‌ها در فایل
def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
