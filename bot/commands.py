from bot.balance import start_balance_flow
from bot.utils import send_message

def handle_command(message, is_group=False):
    chat = message.get("chat", {})
    text = message.get("text", "").strip()
    chat_id = chat.get("id")
    user_id = message.get("from", {}).get("id")

    if not text or not chat_id or not user_id:
        return

    # پیام خوش‌آمد و منوی اصلی
    if text == "/start":
        send_message(chat_id, "👋 خوش آمدید! لطفاً یک گزینه را انتخاب کنید.")

    # افزایش موجودی
    elif text == "💰 افزایش موجودی":
        start_balance_flow(chat_id, user_id)

    # فروشگاه
    elif text == "🛒 فروشگاه":
        send_message(chat_id, "🛍 فروشگاه به‌زودی فعال خواهد شد.")

    # پنل مدیریت
    elif text == "🛠 پنل مدیریت":
        send_message(chat_id, "🛠 پنل مدیریت در حال توسعه است.")

    # حساب کاربری
    elif text == "📨 حساب کاربری":
        send_message(chat_id, "📊 اطلاعات حساب شما به‌زودی اضافه می‌شود.")

    # پشتیبانی
    elif text == "ℹ️ پشتیبانی":
        send_message(chat_id, "📞 پشتیبانی: @CyrusParsy")

    # دستورات نامعتبر
    else:
        send_message(chat_id, "❗ دستور نامعتبر است.")
