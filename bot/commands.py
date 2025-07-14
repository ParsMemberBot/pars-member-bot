from bot.start import handle_start, handle_menu
from bot.admin import handle_admin_panel
from bot.group import handle_group_message
from bot.store import handle_store
from bot.balance import handle_balance_request
from bot.admin_actions import handle_admin_action
from bot.utils import send_message
import re

def handle_command(msg, is_group):
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    text = msg.get("text", "").strip()

    # ✅ دستورات عمومی
    if text.startswith("/start"):
        handle_start(chat_id, user_id)

    elif text in ["منو", "بازگشت"]:
        handle_menu(chat_id, user_id)

    elif text in ["🛍 فروشگاه", "فروشگاه", "سفارش"]:
        handle_store(chat_id, user_id)

    elif text in ["💰 افزایش موجودی"]:
        handle_balance_request(chat_id, user_id)

    elif text in ["💬 پشتیبانی", "پشتیبانی"]:
        send_message(chat_id, "📞 برای پشتیبانی با آیدی زیر تماس بگیرید:\n@CyrusParsy")

    elif text in ["📥 حساب کاربری", "حساب کاربری"]:
        send_message(chat_id, "🚧 بخش حساب کاربری در دست ساخت است.")

    # ✅ فقط در گروه‌ها
    elif is_group and text in ["👮‍♂️ مدیریت گروه", "مدیریت گروه"]:
        handle_group_message(msg)

    elif is_group and text in ["🎮 سرگرمی", "سرگرمی"]:
        send_message(chat_id, "🎉 ارسال سرگرمی فعال شد (در دست ساخت).")

    # ✅ فقط برای ادمین‌ها
    elif text in ["🛠 پنل مدیریت", "پنل مدیریت", "/admin"]:
        handle_admin_panel(chat_id, user_id)

    # ✅ دستورات داخل پنل مدیریت
    elif re.match(r"^(افزودن محصول|افزودن دسته|لیست سفارشات|مدیریت کاربران|تنظیمات ربات|📨 پیام همگانی)$", text):
        handle_admin_action(chat_id, user_id, text)

    else:
        send_message(chat_id, "❗️ دستور نامعتبر است. لطفاً از منو استفاده کنید.")
