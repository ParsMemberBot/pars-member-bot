from bot.utils import send_message
from bot.store import handle_store
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.fun import handle_fun_commands  # اصلاح اسم تابع

def handle_command(message, is_group=False):
    if not message:
        return

    chat = message.get("chat", {})
    user = message.get("from", {})
    text = message.get("text", "").strip()

    chat_id = chat.get("id")
    user_id = user.get("id")

    if not chat_id or not user_id:
        return  # جلوگیری از ارور در صورت ناقص بودن داده‌ها

    if is_group:
        handle_group_message(message)
        return

    if text == "/start":
        send_main_menu(chat_id)
    elif "فروشگاه" in text:
        handle_store(chat_id, user_id)
    elif "پنل مدیریت" in text:
        handle_admin_panel(chat_id, user_id)
    elif text in ["جوک", "فال"] or text.startswith("/ai") or text.startswith("هوش مصنوعی") or text.startswith("ربات"):
        handle_fun_commands(message)
    else:
        send_message(chat_id, "❗️دستور نامعتبر است. لطفاً از منو استفاده کنید.")

def send_main_menu(chat_id):
    buttons = [
        [{"text": "🛍 فروشگاه"}, {"text": "🎉 سرگرمی"}],
        [{"text": "📞 پشتیبانی"}, {"text": "⚙️ پنل مدیریت"}]
    ]
    reply_markup = {
        "keyboard": buttons,
        "resize_keyboard": True
    }
    send_message(chat_id, "از منوی زیر استفاده کنید:", reply_markup)
