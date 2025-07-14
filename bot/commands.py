from bot.menu import send_main_menu
from bot.admin_actions import handle_admin_action
from bot.balance import handle_balance_request, handle_balance_step
from bot.shop import handle_shop_action
from bot.group import handle_group_command
from bot.users import check_or_create_user

def is_admin_action(text):
    return text in [
        '🛠 پنل مدیریت', '📦 افزودن محصول', '📂 افزودن دسته‌بندی',
        '🧾 لیست سفارشات', '👤 مدیریت کاربران', '◀️ بازگشت',
        '➕ افزودن موجودی', '📊 آمار', '🔙 منوی اصلی'
    ]

def is_user_command(text):
    return text in [
        '💰 افزایش موجودی', '🛒 فروشگاه', '🧾 سفارشات من', '💼 حساب کاربری', '💬 پشتیبانی'
    ]

def handle_command(message, is_group=False):
    chat_id = message['chat']['id']
    user_id = message['from']['id']
    text = message.get('text', '')

    # بررسی و ساخت کاربر در صورت عدم وجود
    check_or_create_user(user_id)

    if is_group:
        handle_group_command(message)
        return

    if text == '/start' or text == '🔙 منوی اصلی':
        send_main_menu(chat_id)
    
    elif text == '💼 حساب کاربری':
        from bot.users import handle_account
        handle_account(chat_id, user_id)
    
    elif text == '💰 افزایش موجودی':
        handle_balance_step(chat_id, user_id, text)

    elif text == '🛒 فروشگاه':
        handle_shop_action(chat_id, user_id, text)

    elif text == '💬 پشتیبانی':
        from bot.support import handle_support
        handle_support(chat_id)

    elif is_admin_action(text):
        handle_admin_action(chat_id, user_id, text)

    elif is_user_command(text):
        # اگر دستور کاربری معتبر بود ولی هنوز پیاده‌سازی نشده
        from bot.utils import send_message
        send_message(chat_id, "در حال ساخت این بخش هستیم...")

    else:
        from bot.utils import send_message
        send_message(chat_id, "❗️دستور نامعتبر است. لطفاً از منو استفاده کنید.")
