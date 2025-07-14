from bot.utils import send_message
from bot.buttons import main_menu_keyboard

def handle_start(chat_id, user_id):
    send_message(chat_id, "✨ به ربات خوش آمدید!", reply_markup=main_menu_keyboard(user_id))

def handle_menu(chat_id, user_id, is_group=False):
    send_message(chat_id, "🔘 منوی اصلی:", reply_markup=main_menu_keyboard(user_id, is_group))
