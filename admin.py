from bot.utils import load_data, save_data, send_message

def handle_admin_panel(chat_id, user_id):
    settings = load_data("data/settings.json")
    admins = settings.get("admins", [])
    if user_id not in admins:
        send_message(chat_id, "شما به پنل مدیریت دسترسی ندارید.")
        return

    buttons = [
        [{"text": "📦 افزودن محصول"}],
        [{"text": "📁 افزودن دسته‌بندی"}],
        [{"text": "🧾 لیست سفارشات"}],
        [{"text": "👤 مدیریت کاربران"}],
        [{"text": "📨 پیام همگانی"}],
        [{"text": "⚙️ تنظیمات ربات"}],
        [{"text": "بازگشت"}]
    ]
    send_message(chat_id, "به پنل مدیریت خوش آمدید:", {"keyboard": buttons, "resize_keyboard": True})