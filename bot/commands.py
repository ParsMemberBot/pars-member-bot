from bot.utils import send_message
from bot.store import handle_store
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.fun import handle_fun_commands
from bot.buttons import main_menu_keyboard
from bot.commands import handle_start, handle_menu

def handle_command(message, is_group=False):
    if not message:
        return

    chat = message.get("chat", {})
    user = message.get("from", {})
    text = message.get("text", "").strip()

    chat_id = chat.get("id")
    user_id = user.get("id")

    if not chat_id or not user_id:
        return

    if is_group:
        handle_group_message(message)
        return

    if text == "/start":
        handle_start(chat_id, user_id)
    elif text in ["منو", "بازگشت"]:
        handle_menu(chat_id, user_id)
    elif "فروشگاه" in text:
        handle_store(chat_id, user_id)
    elif "پنل مدیریت" in text:
        handle_admin_panel(chat_id, user_id)
    elif "سرگرمی" in text or text in ["جوک", "فال", "/ai", "هوش مصنوعی", "ربات"]:
        handle_fun_commands(message)
    elif "حساب" in text:
        send_message(chat_id, "💼 اطلاعات حساب شما اینجاست...")
    elif "پشتیبانی" in text:
        send_message(chat_id, "📞 برای پشتیبانی با @CyrusParsy در ارتباط باشید.")
    elif "مدیریت گروه" in text:
        send_message(chat_id, "🔧 وارد بخش مدیریت گروه شدید. فعلاً دستورات را تایپ کنید.")
    else:
        send_message(chat_id, "❗️دستور نامعتبر است. لطفاً از منو استفاده کنید.")
