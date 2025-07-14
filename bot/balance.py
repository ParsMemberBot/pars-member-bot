from bot.utils import send_message, load_data, save_data
import os

def start_balance_flow(chat_id, user_id):
    users = load_data("data/users.json")
    if str(user_id) not in users:
        users[str(user_id)] = {"balance": 0, "orders": []}
        save_data("data/users.json", users)

    # وضعیت مرحله‌ای برای وارد کردن مبلغ
    step_file = f"data/step/{user_id}.json"
    os.makedirs("data/step", exist_ok=True)
    save_data(step_file, {"step": "balance_amount"})

    send_message(chat_id, "💳 لطفاً مبلغ مورد نظر برای افزایش موجودی را وارد کنید:")
