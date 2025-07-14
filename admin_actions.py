
from bot.utils import send_message

def handle_admin_action(chat_id, user_id, text):
    if text == "📦 افزودن محصول":
        send_message(chat_id, "📝 لطفاً اطلاعات محصول جدید را وارد کنید.")
    elif text == "📁 افزودن دسته‌بندی":
        send_message(chat_id, "📂 لطفاً نام دسته‌بندی جدید را وارد کنید.")
    elif text == "🧾 لیست سفارشات":
        send_message(chat_id, "📋 نمایش لیست سفارشات در دست ساخت است.")
    elif text == "👤 مدیریت کاربران":
        send_message(chat_id, "👥 بخش مدیریت کاربران در دست ساخت است.")
    elif text == "📨 پیام همگانی":
        send_message(chat_id, "🗣 لطفاً پیام مورد نظر خود را برای ارسال به همه کاربران وارد کنید.")
    elif text == "⚙️ تنظیمات ربات":
        send_message(chat_id, "⚙️ بخش تنظیمات ربات در دست ساخت است.")
    else:
        send_message(chat_id, "❗️دستور مدیریتی ناشناخته است.")
