import json
import requests
from bot.config import TOKEN

API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

# بارگذاری دیتا از فایل JSON
def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [] if file_path.endswith(".json") else {}

# ذخیره دیتا در فایل JSON
def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ارسال پیام ساده
def send_message(chat_id, text):
    if not text or not chat_id:
        print("⚠️ پیام یا chat_id خالی است.")
        return
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(API_URL + "sendMessage", json=payload)
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)

# ارسال پیام همراه دکمه‌های تعاملی
def send_buttons(chat_id, text, buttons):
    if not text or not chat_id:
        print("⚠️ متن یا chat_id برای دکمه خالی است.")
        return
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": buttons
        }
    }
    try:
        requests.post(API_URL + "sendMessage", json=payload)
    except Exception as e:
        print("❌ خطا در ارسال دکمه‌ها:", e)

# ویرایش پیام قبلی با متن جدید و دکمه‌ها
def edit_message(chat_id, message_id, text, buttons=None):
    if not chat_id or not message_id:
        print("⚠️ chat_id یا message_id نامعتبر است.")
        return
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }
    if buttons:
        payload["reply_markup"] = {
            "inline_keyboard": buttons
        }
    try:
        requests.post(API_URL + "editMessageText", json=payload)
    except Exception as e:
        print("❌ خطا در ویرایش پیام:", e)

# منوی اصلی برای کاربران
def send_menu(chat_id):
    text = "به منوی اصلی ربات خوش آمدید 🌟"
    buttons = [
        [{"text": "🛒 فروشگاه", "callback_data": "shop"}],
        [{"text": "👤 حساب کاربری", "callback_data": "account"}],
        [{"text": "🛠 مدیریت گروه", "callback_data": "group"}],
        [{"text": "📞 پشتیبانی", "callback_data": "support"}]
    ]
    send_buttons(chat_id, text, buttons)

# تبدیل آیدی عددی به لینک کاربر (برای پیام‌های مدیر)
def user_link(user):
    if user.get("username"):
        return f"@{user['username']}"
    return f"[{user.get('first_name', 'کاربر') or 'کاربر'}](tg://user?id={user['id']})"
