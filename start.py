import time
from bot.handlers import handle_message
from bot.utils import load_users, save_users
from bot.bale import get_updates, send_message

last_update_id = 0
users = load_users()

def main():
    global last_update_id
    print("✅ ربات با موفقیت اجرا شد.")

    while True:
        try:
            updates = get_updates(last_update_id)
            for update in updates:
                if 'message' in update:
                    msg = update['message']
                    user_id = str(msg['chat']['id'])

                    if user_id not in users:
                        users[user_id] = {
                            "balance": 0,
                            "orders": [],
                            "warns": 0,
                            "blocked": False
                        }
                        save_users(users)

                    handle_message(msg, users)
                    last_update_id = update['update_id'] + 1

        except Exception as e:
            print("❌ خطا:", e)

        time.sleep(1)

if __name__ == "__main__":
    main()
