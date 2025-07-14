from bot.utils import send_message, load_data, save_data
from bot.buttons import main_menu_keyboard

def handle_start(chat_id, user_id):
    users = load_data("data/users.json")
    if str(user_id) not in users:
        users[str(user_id)] = {
            "balance": 0,
            "orders": [],
            "warns": 0
        }
        save_data("data/users.json", users)

    text = "👋 خوش آمدید!\nبه ربات فروش خدمات و مدیریت گروه خوش آمدید."
    send_message(chat_id, text, reply_markup=main_menu_keyboard())

def handle_menu(chat_id, user_id):
    text = "📋 منوی اصلی را انتخاب کنید:"
    send_message(chat_id, text, reply_markup=main_menu_keyboard())
