from bot.utils import load_data

def main_menu_keyboard(user_id=None, is_group=False):
    buttons = [
        [{"text": "🛍 فروشگاه"}, {"text": "📥 حساب کاربری"}],
        [{"text": "💵 افزایش موجودی"}],
        [{"text": "💬 پشتیبانی"}]
    ]

    if is_group:
        buttons.insert(1, [{"text": "👮‍♂️ مدیریت گروه"}, {"text": "🎮 سرگرمی"}])

    if user_id:
        settings = load_data("data/settings.json")
        admins = settings.get("admins", [])
        if str(user_id) in map(str, admins):
            buttons.insert(-1, [{"text": "🛠 پنل مدیریت"}])

    return {
        "keyboard": buttons,
        "resize_keyboard": True
    }
