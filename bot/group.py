import json
import re
from utils import send_message, kick_user

WELCOME_MESSAGE = "خوش آمدی به گروه!"
ANTI_LINK = True

def handle_group_message(message):
    text = message.get("text", "")
    group_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    username = message["from"].get("username", "ناشناس")

    # خوش‌آمدگویی به کاربران جدید
    if "new_chat_members" in message:
        for member in message["new_chat_members"]:
            send_message(group_id, f"{member['first_name']} عزیز، {WELCOME_MESSAGE}")
        return

    # ضد لینک
    if ANTI_LINK and re.search(r"(https?://|t\.me|ble\.ir|@[\w_]+)", text):
        send_message(group_id, "❗️ارسال لینک ممنوع است.")
        kick_user(group_id, user_id)

    # دستورات فارسی مدیریت گروه
    if text == "اخراج":
        reply = message.get("reply_to_message")
        if reply:
            target_id = reply["from"]["id"]
            kick_user(group_id, target_id)
            send_message(group_id, f"✅ کاربر اخراج شد.")
        else:
            send_message(group_id, "❗️برای اخراج باید روی پیام فرد ریپلای کنید.")

    elif text == "ضد لینک روشن":
        global ANTI_LINK
        ANTI_LINK = True
        send_message(group_id, "✅ ضد لینک فعال شد.")

    elif text == "ضد لینک خاموش":
        ANTI_LINK = False
        send_message(group_id, "❌ ضد لینک غیرفعال شد.")

    elif text.startswith("تنظیم خوش‌آمد"):
        global WELCOME_MESSAGE
        WELCOME_MESSAGE = text.replace("تنظیم خوش‌آمد", "").strip()
        send_message(group_id, f"✅ پیام خوش‌آمد تنظیم شد:\n{WELCOME_MESSAGE}")
