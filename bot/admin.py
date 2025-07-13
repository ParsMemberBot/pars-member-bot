from bot.utils import load_data, save_data, send_message

def handle_admin_panel(chat_id, user_id):
    settings = load_data("data/settings.json") or {}
    admins = settings.get("admins", [])

    # بررسی دسترسی
    if str(user_id) not in [str(admin) for admin in admins]:
        send_message(chat_id, "❌ شما به پنل مدیریت دسترسی ندارید.")
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

    reply_markup = {
        "keyboard": buttons,
        "resize_keyboard": True
    }
    send_message(chat_id, "👋 به پنل مدیریت خوش آمدید:", reply_markup)
