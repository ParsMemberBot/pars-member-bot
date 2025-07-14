from bot.start import handle_start, handle_menu
from bot.admin import handle_admin_panel
from bot.admin_actions import handle_admin_actions
from bot.group import handle_group_message
from bot.store import handle_store
from bot.utils import send_message, load_data
from bot.balance import start_balance_flow, handle_balance_step

# وضعیت کاربران ذخیره میشه برای مراحل بعدی
user_states = {}

def handle_command(msg, is_group):
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    text = msg.get("text", "")

    # مرحله بعد از شروع افزایش موجودی
    if user_id in user_states:
        step = user_states.pop(user_id)
        if step == "awaiting_balance_amount":
            handle_balance_step(chat_id, user_id, text)
            return

    if text.startswith("/start"):
        handle_start(chat_id, user_id)

    elif text in ["منو", "بازگشت"]:
        handle_menu(chat_id, user_id)

    elif text in ["🛍 فروشگاه", "فروشگاه", "سفارش"]:
        handle_store(chat_id, user_id)

    elif text in ["📥 حساب کاربری", "حساب کاربری"]:
        send_message(chat_id, "🚧 بخش حساب کاربری در دست ساخت است.")

    elif text in ["💬 پشتیبانی", "پشتیبانی"]:
        send_message(chat_id, "📞 برای پشتیبانی با آیدی زیر تماس بگیرید:\n@CyrusParsy")

    elif text in ["🛠 پنل مدیریت", "پنل مدیریت", "/admin"]:
        handle_admin_panel(chat_id, user_id)

    elif text in ["👮‍♂️ مدیریت گروه", "مدیریت گروه"] and is_group:
        handle_group_message(msg)

    elif text in ["💰 افزایش موجودی", "افزایش موجودی"]:
        user_states[user_id] = "awaiting_balance_amount"
        send_message(chat_id, "🔢 لطفاً مبلغ مورد نظر برای افزایش موجودی را وارد کنید.")

    # دستورات داخل پنل مدیریت
    elif text in [
        "📦 افزودن محصول", "💳 افزایش دستی موجودی", "📋 لیست سفارشات",
        "👥 مدیریت کاربران", "⚙️ تنظیمات ربات", "✉️ پیام همگانی"
    ]:
        handle_admin_actions(chat_id, user_id, text)

    else:
        send_message(chat_id, "❗️ دستور نامعتبر است. لطفاً از منو استفاده کنید.")
