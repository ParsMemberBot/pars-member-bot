from bot.utils import load_data

def main_menu_keyboard(user_id=None, is_group=False):
    buttons = []

    # دکمه‌های عمومی
    row1 = [{"text": "🛍 فروشگاه"}, {"text": "📥 حساب کاربری"}]
    row2 = []

    if not is_group:
        row2.append({"text": "💰 افزایش موجودی"})
    if is_group:
        row2.append({"text": "👮‍♂️ مدیریت گروه"})
    else:
        row2.append({"text": "🎮 سرگرمی"})

    row3 = [{"text": "💬 پشتیبانی"}]

    # بررسی ادمین بودن برای نمایش دکمه مدیریت
    if user_id:
        settings = load_data("data/settings.json")
        admins = settings.get("admins", [])
        if str(user_id) in [str(admin) for admin in admins]:
            row3.insert(0, {"text": "🛠 پنل مدیریت"})

    buttons.append(row1)
    if row2:
        buttons.append(row2)
    buttons.append(row3)

    return {
        "keyboard": buttons,
        "resize_keyboard": True
    }
