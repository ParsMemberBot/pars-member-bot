import re
from utils import send_message, kick_user

# تنظیمات سراسری (غیرفردی)
WELCOME_MESSAGE = "خوش آمدی به گروه!"
ANTI_LINK = True

def handle_group_message(message):
    global WELCOME_MESSAGE, ANTI_LINK

    # بررسی پایه‌ای برای جلوگیری از ارورهای KeyError
    if "chat" not in message or "from" not in message:
        return

    text = message.get("text", "").strip()
    group_id = message["chat"].get("id")
    user_id = message["from"].get("id")
    username = message["from"].get("username", "ناشناس")

    if not group_id or not user_id:
        return

    # خوش‌آمدگویی به کاربران جدید
    if "new_chat_members" in message:
        for member in message["new_chat_members"]:
            name = member.get("first_name", "کاربر جدید")
            send_message(group_id, f"{name} عزیز، {WELCOME_MESSAGE}")
        return

    # ضد لینک (پیام حاوی لینک)
    if ANTI_LINK and re.search(r"(https?://|t\.me|ble\.ir|@[\w_]+)", text):
        send_message(group_id, "❗️ارسال لینک ممنوع است.")
        kick_user(group_id, user_id)
        return

    # مدیریت گروه - دستورات فارسی
    if text == "اخراج":
        reply = message.get("reply_to_message")
        if reply and "from" in reply:
            target_id = reply["from"].get("id")
            if target_id:
                kick_user(group_id, target_id)
                send_message(group_id, "✅ کاربر با موفقیت اخراج شد.")
            else:
                send_message(group_id, "❗️شناسه کاربر یافت نشد.")
        else:
            send_message(group_id, "❗️برای اخراج، باید روی پیام فرد ریپلای کنید.")

    elif text == "ضد لینک روشن":
        ANTI_LINK = True
        send_message(group_id, "✅ ضد لینک فعال شد.")

    elif text == "ضد لینک خاموش":
        ANTI_LINK = False
        send_message(group_id, "❌ ضد لینک غیرفعال شد.")

    elif text.startswith("تنظیم خوش‌آمد"):
        new_msg = text.replace("تنظیم خوش‌آمد", "").strip()
        if new_msg:
            WELCOME_MESSAGE = new_msg
            send_message(group_id, f"✅ پیام خوش‌آمد جدید تنظیم شد:\n{WELCOME_MESSAGE}")
        else:
            send_message(group_id, "❗️لطفاً متن پیام خوش‌آمد را وارد کنید.")
