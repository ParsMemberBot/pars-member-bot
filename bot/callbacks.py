from bot.utils import send_message, load_data, save_data, edit_message
from bot.config import ORDER_CHANNEL_ID, BALANCE_CHANNEL_ID, SUPPORT_IDS

def handle_callback_query(callback_query):
    data = callback_query.get("data", "")
    user = callback_query.get("from", {})
    message = callback_query.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    msg_id = message.get("message_id")

    if not data:
        return

    # ✅ دکمه‌های منوی اصلی
    if data == "shop":
        send_message(chat_id, "🛍 به فروشگاه خوش آمدید!\n(در حال توسعه...)")
        return

    elif data == "account":
        send_message(chat_id, "👤 اطلاعات حساب شما به زودی در دسترس خواهد بود.")
        return

    elif data == "group":
        send_message(chat_id, "🛠 ابزارهای مدیریت گروه فعال نیستند.")
        return

    elif data == "support":
        support = "\n".join(SUPPORT_IDS)
        send_message(chat_id, f"📞 پشتیبانی:\n{support}")
        return

    # ⚠️ اگر دکمه‌ معتبر نیست
    if ":" not in data:
        send_message(chat_id, "❗ فرمان دکمه نامعتبر است.")
        return

    # 🔽 دکمه‌های با داده‌های خاص (تأیید/رد سفارش یا موجودی)
    parts = data.split(":")
    action = parts[0]

    if action == "order_accept" and len(parts) == 3:
        user_id = int(parts[1])
        order_id = parts[2]

        orders = load_data("data/orders.json")
        for o in orders:
            if o["id"] == order_id:
                o["status"] = "تایید شده"
                save_data("data/orders.json", orders)
                text = message["text"] + "\n✅ سفارش تایید شد."
                edit_message(ORDER_CHANNEL_ID, msg_id, text)
                send_message(user_id, "✅ سفارش شما تایید شد.")
                break

    elif action == "order_reject" and len(parts) == 3:
        user_id = int(parts[1])
        order_id = parts[2]

        orders = load_data("data/orders.json")
        for o in orders:
            if o["id"] == order_id:
                o["status"] = "رد شده"
                save_data("data/orders.json", orders)
                text = message["text"] + "\n❌ سفارش رد شد."
                edit_message(ORDER_CHANNEL_ID, msg_id, text)
                send_message(user_id, "❌ سفارش شما رد شد.")
                break

    elif action == "balance_accept" and len(parts) == 3:
        user_id = int(parts[1])
        amount = int(parts[2])

        users = load_data("data/users.json")
        for u in users:
            if u["user_id"] == user_id:
                u["balance"] += amount
                break
        else:
            users.append({"user_id": user_id, "balance": amount})

        save_data("data/users.json", users)
        text = message["text"] + "\n✅ افزایش موجودی تایید شد."
        edit_message(BALANCE_CHANNEL_ID, msg_id, text)
        send_message(user_id, f"✅ موجودی شما {amount} تومان افزایش یافت.")

    elif action == "balance_reject" and len(parts) == 2:
        user_id = int(parts[1])
        text = message["text"] + "\n❌ افزایش موجودی رد شد."
        edit_message(BALANCE_CHANNEL_ID, msg_id, text)
        send_message(user_id, "❌ افزایش موجودی شما رد شد.")
