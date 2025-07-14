from bot.utils import send_message
from bot.start import handle_start, handle_menu
from bot.store import handle_store
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.fun import handle_fun_commands

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
    elif text in ["جوک", "فال"] or text.startswith("/ai") or text.startswith("هوش مصنوعی") or text.startswith("ربات"):
        handle_fun_commands(message)
    else:
        send_message(chat_id, "❗️دستور نامعتبر است. لطفاً از منو استفاده کنید.")
