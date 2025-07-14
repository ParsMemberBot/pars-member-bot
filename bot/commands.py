from bot.start import handle_start, handle_menu
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.store import handle_store
from bot.utils import send_message

def handle_command(msg, is_group):
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    text = msg.get("text", "")

    if text.startswith("/start"):
        handle_start(chat_id, user_id)
    elif text in ["منو", "بازگشت"]:
        handle_menu(chat_id, user_id)
    elif text in ["🛍 فروشگاه", "فروشگاه", "سفارش"]:
        handle_store(chat_id, user_id)
    elif text in ["🛠 پنل مدیریت", "پنل مدیریت", "/admin"]:
        handle_admin_panel(chat_id, user_id)
    elif text in ["👮‍♂️ مدیریت گروه", "مدیریت گروه"]:
        handle_group_message(msg)
    elif text in ["📥 حساب کاربری", "حساب کاربری"]:
        send_message(chat_id, "🚧 بخش حساب کاربری در دست ساخت است.")
    elif text in ["💬 پشتیبانی", "پشتیبانی"]:
        send_message(chat_id, "📞 برای پشتیبانی با آیدی زیر تماس بگیرید:\n@CyrusParsy")
    else:
        send_message(chat_id, "❗️ دستور نامعتبر است. لطفاً از منو استفاده کنید.")
