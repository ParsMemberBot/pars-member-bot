from bot.utils import load_data

def main_menu_keyboard(user_id=None, is_group=False):
    # دکمه‌های پایه برای همه کاربران
    buttons = [
        [{"text": "🛍 فروشگاه"}, {"text": "📥 حساب کاربری"}],
        [{"text": "💵 افزایش موجودی"}],
        [{"text": "💬 پشتیبانی"}]
    ]

    # فقط در گروه: دکمه‌های گروهی
    if is_group:
        buttons.insert(1, [{"text": "👮‍♂️ مدیریت گروه"}, {"text": "🎮 سرگرمی"}])

    # فقط برای ادمین‌ها: دکمه پنل مدیریت
    if user_id:
        settings = load_data("data/settings.json")
        admins = settings.get("admins", [])
        if str(user_id) in [str(admin) for admin in admins]:
            buttons.insert(-1, [{"text": "🛠 پنل مدیریت"}])

    return {
        "keyboard": buttons,
        "resize_keyboard": True
    }
