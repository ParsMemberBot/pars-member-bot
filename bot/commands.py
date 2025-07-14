from bot.utils import send_message
from bot.balance import start_balance_flow
from bot.orders import start_order_flow
from bot.config import SUPPORT_IDS

def handle_command(message, is_group=False):
    chat = message.get("chat", {})
    text = message.get("text", "").strip()
    chat_id = chat.get("id")
    user_id = message.get("from", {}).get("id")

    if not text or not chat_id or not user_id:
        return

    # پاسخ به /start
    if text == "/start":
        send_message(chat_id, "👋 خوش آمدید! لطفاً از منوی زیر انتخاب کنید:")
        send_menu(chat_id)
        return

    # دستورات منو
    if text == "💰 افزایش موجودی":
        start_balance_flow(chat_id, user_id)
        return

    if text == "🛒 ثبت سفارش":
        start_order_flow(chat_id, user_id)
        return

    if text == "📩 حساب کاربری":
        send_message(chat_id, "📬 اطلاعات حساب کاربری شما به‌زودی اضافه می‌شود.")
        return

    if text == "🔧 پنل مدیریت":
        send_message(chat_id, "🛠 پنل مدیریت در حال توسعه است.")
        return

    if text == "ℹ️ پشتیبانی":
        support = "\n".join(SUPPORT_IDS)
        send_message(chat_id, f"📞 پشتیبانی:\n{support}")
        return

    # اگر دستور ناشناخته بود
    send_message(chat_id, "❗ دستور نامعتبر است.")
