from bot.utils import send_message, send_menu, load_data
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

    # دکمه افزایش موجودی
    if text == "💰 افزایش موجودی":
        start_balance_flow(chat_id, user_id)
        return

    # دکمه ثبت سفارش
    if text == "🛒 ثبت سفارش":
        start_order_flow(chat_id, user_id)
        return

    # دکمه حساب کاربری
    if text == "📩 حساب کاربری":
        show_account(chat_id, user_id)
        return

    # دکمه فروشگاه
    if text == "🛍 فروشگاه":
        show_shop(chat_id)
        return

    # دکمه پشتیبانی
    if text == "💬 پشتیبانی" or text == "ℹ️ پشتیبانی":
        support = "\n".join(SUPPORT_IDS)
        send_message(chat_id, f"📞 پشتیبانی:\n{support}")
        return

    # دکمه پنل مدیریت (فعلاً در حال توسعه)
    if text == "🔧 پنل مدیریت":
        send_message(chat_id, "🛠 پنل مدیریت در حال توسعه است.")
        return

    # پاسخ پیش‌فرض
    send_message(chat_id, "❗ دستور نامعتبر است.")


def show_account(chat_id, user_id):
    users = load_data("data/users.json")
    user = users.get(str(user_id), {"balance": 0, "orders": []})
    balance = user.get("balance", 0)
    orders = user.get("orders", [])

    text = f"""📬 اطلاعات حساب شما:

🆔 آیدی عددی: {user_id}
💰 موجودی: {balance} تومان
📦 تعداد سفارش‌ها: {len(orders)}
"""
    send_message(chat_id, text)


def show_shop(chat_id):
    text = "🛍 دسته‌بندی محصولات:\n\nلطفاً یکی از گزینه‌ها را انتخاب کنید:"
    keyboard = {
        "keyboard": [
            [{"text": "🔹 ممبر واقعی"}, {"text": "🔹 فالوور اینستاگرام"}],
            [{"text": "🔙 بازگشت به منو"}]
        ],
        "resize_keyboard": True
    }
    send_message(chat_id, text, reply_markup=keyboard)
