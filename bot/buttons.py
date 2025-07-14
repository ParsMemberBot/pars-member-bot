from bot.utils import load_data

def main_menu_keyboard(user_id=None):
    # منوی عمومی برای همه
    buttons = [
        [{"text": "🛍 فروشگاه"}, {"text": "📥 حساب کاربری"}],
        [{"text": "👮‍♂️ مدیریت گروه"}, {"text": "🎮 سرگرمی"}],
        [{"text": "💬 پشتیبانی"}]
    ]

    # بررسی اگر user_id جزو adminها باشد → دکمه پنل مدیریت را اضافه کن
    if user_id:
        settings = load_data("data/settings.json")
        admins = settings.get("admins", [])
        if str(user_id) in [str(admin) for admin in admins]:
            buttons.insert(-1, [{"text": "🛠 پنل مدیریت"}])  # قبل از پشتیبانی اضافه کن

    return {
        "keyboard": buttons,
        "resize_keyboard": True
    }
