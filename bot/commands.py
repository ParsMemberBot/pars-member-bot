from bot.utils import send_message
from bot.admin_actions import handle_admin_action
from bot.balance import start_balance_flow, handle_balance_step
from bot.orders import start_order_flow, handle_order_step

def send_main_menu(chat_id):
    keyboard = [
        [{"text": "📩 حساب کاربری"}, {"text": "💰 افزایش موجودی"}],
        [{"text": "🛍️ فروشگاه"}, {"text": "💬 پشتیبانی"}],
        [{"text": "🛠 پنل مدیریت"}]
    ]
    send_message(chat_id, "⚪ منوی اصلی:", keyboard=keyboard)

def handle_command(message, is_group=False):
    text = message.get("text")
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]

    if not text:
        return

    if text.startswith("/start"):
        send_message(chat_id, "✨ به ربات خوش آمدید!")
        send_main_menu(chat_id)

    elif text == "📩 حساب کاربری":
        send_message(chat_id, "🚧 بخش حساب کاربری در دست ساخت است.")

    elif text == "💬 پشتیبانی":
        send_message(chat_id, "📞 برای پشتیبانی با آیدی زیر تماس بگیرید:\n@CyrusParsy")

    elif text == "💰 افزایش موجودی":
        start_balance_flow(chat_id, user_id)

    elif text == "🛍️ فروشگاه":
        send_message(chat_id, "هیچ دسته‌بندی‌ای در فروشگاه ثبت نشده است.")

    elif text == "🛠 پنل مدیریت":
        send_message(chat_id, "👋 به پنل مدیریت خوش آمدید:")

    elif text == "⚪ منوی اصلی":
        send_main_menu(chat_id)

    elif text.startswith("بازگشت"):
        send_main_menu(chat_id)

    else:
        # بررسی فلوها
        if is_group:
            return

        if text.startswith("/ai") or "هوش مصنوعی" in text or "ربات" in text:
            send_message(chat_id, "🤖 این بخش هنوز فعال نشده است.")
            return

        if text.replace(" ", "").isdigit():
            handle_balance_step(chat_id, user_id, text)
            return

        send_message(chat_id, "❗️ دستور نامعتبر است. لطفاً از منو استفاده کنید.")
