from bot.utils import send_message
from bot.store import handle_store
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.fun import handle_fun

def handle_command(chat_id, user_id, text, is_group=False):
    if is_group:
        handle_group_message(chat_id, user_id, text)
        return

    if text == "/start":
        send_main_menu(chat_id)
    elif "فروشگاه" in text:
        handle_store(chat_id, user_id)
    elif "پنل مدیریت" in text:
        handle_admin_panel(chat_id, user_id)
    elif text in ["جوک", "فال", "/ai", "هوش مصنوعی", "ربات"]:
        handle_fun(chat_id, user_id, text)
    else:
        send_message(chat_id, "دستور نامعتبر است.")

def send_main_menu(chat_id):
    buttons = [
        [{"text": "🛍 فروشگاه"}, {"text": "🎉 سرگرمی"}],
        [{"text": "📞 پشتیبانی"}, {"text": "⚙️ پنل مدیریت"}]
    ]
    send_message(chat_id, "از منوی زیر استفاده کنید:", {"keyboard": buttons, "resize_keyboard": True})
