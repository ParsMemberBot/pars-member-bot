from bot.utils import send_message
from bot.balance import start_balance_flow

def handle_command(message, is_group=False):
    chat = message.get("chat", {})
    text = message.get("text", "").strip()
    chat_id = chat.get("id")
    user_id = message.get("from", {}).get("id")

    if not text or not chat_id or not user_id:
        return

    # پاسخ به /start
    if text == "/start":
        send_message(
            chat_id,
            "👋 خوش آمدید! لطفاً یک گزینه را انتخاب کنید.",
            reply_markup={
                "keyboard": [
                    [{"text": "💰 افزایش موجودی"}],
                    [{"text": "🛍 فروشگاه"}, {"text": "📩 حساب کاربری"}],
                    [{"text": "🔧 پنل مدیریت"}, {"text": "💬 پشتیبانی"}],
                ],
                "resize_keyboard": True
            }
        )
        return

    # دستورات دکمه‌ها
    if text == "💰 افزایش موجودی":
        start_balance_flow(chat_id, user_id)
        return

    if text == "🛍 فروشگاه":
        send_message(chat_id, "🛒 فروشگاه به‌زودی فعال می‌شود.")
        return

    if text == "📩 حساب کاربری":
        send_message(chat_id, "📬 اطلاعات حساب کاربری شما به‌زودی نمایش داده می‌شود.")
        return

    if text == "🔧 پنل مدیریت":
        send_message(chat_id, "🔧 پنل مدیریت در حال توسعه است.")
        return

    if text == "💬 پشتیبانی":
        send_message(chat_id, "📞 ارتباط با پشتیبانی: @CyrusParsy")
        return

    # پاسخ پیش‌فرض برای دستورات ناشناخته
    send_message(chat_id, "❗دستور نامعتبر است.")
