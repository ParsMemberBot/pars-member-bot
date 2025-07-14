from bot.utils import send_message
from bot.buttons import main_menu_keyboard
from bot.utils import load_data

def handle_start(chat_id, user_id):
    settings = load_data("data/settings.json")
    welcome = settings.get("welcome_message", "سلام! به ربات خوش آمدید.")
    reply_markup = main_menu_keyboard(user_id)
    send_message(chat_id, welcome, reply_markup)

def handle_menu(chat_id, user_id, is_group=False):
    reply_markup = main_menu_keyboard(user_id, is_group)
    send_message(chat_id, "🔘 منوی اصلی:", reply_markup)
