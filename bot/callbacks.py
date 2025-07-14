import json
import requests
from bot.utils import send_message, load_data, save_data
from bot.main import API_URL

USERS_FILE = "data/users.json"
ORDERS_FILE = "data/orders.json"

def handle_callback_query(callback_query):
    data = callback_query.get("data")
    msg = callback_query.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    message_id = msg.get("message_id")
    from_id = callback_query.get("from", {}).get("id")

    if data.startswith("balance_accept:"):
        _, user_id, amount, req_id = data.split(":")
        user_id = int(user_id)
        amount = int(amount)

        users = load_data(USERS_FILE)
        if str(user_id) not in users:
            users[str(user_id)] = {"balance": 0, "orders": []}

        users[str(user_id)]["balance"] += amount
        save_data(USERS_FILE, users)

        send_message(user_id, f"✅ افزایش موجودی شما به مبلغ {amount} تومان تأیید شد.")
        new_text = msg.get("text", "") + f"\n\n✅ توسط مدیر تأیید شد."
        requests.post(API_URL + "editMessageText", json={
            "chat_id": chat_id,
            "message_id": message_id,
            "text": new_text
        })

    elif data.startswith("balance_reject:"):
        _, user_id, amount, req_id = data.split(":")
        user_id = int(user_id)

        send_message(user_id, f"❌ افزایش موجودی شما به مبلغ {amount} تومان رد شد.")
        new_text = msg.get("text", "") + f"\n\n❌ توسط مدیر رد شد."
        requests.post(API_URL + "editMessageText", json={
            "chat_id": chat_id,
            "message_id": message_id,
            "text": new_text
        })

    elif data.startswith("order_accept:"):
        _, user_id, order_id = data.split(":")
        user_id = int(user_id)

        orders = load_data(ORDERS_FILE)
        order = next((o for o in orders if o["id"] == order_id), None)

        if order:
            order["status"] = "done"
            save_data(ORDERS_FILE, orders)
            send_message(user_id, f"✅ سفارش شما با شناسه {order_id} تأیید شد و در حال انجام است.")
            new_text = msg.get("text", "") + "\n\n✅ توسط مدیر تأیید شد."
            requests.post(API_URL + "editMessageText", json={
                "chat_id": chat_id,
                "message_id": message_id,
                "text": new_text
            })

    elif data.startswith("order_reject:"):
        _, user_id, order_id = data.split(":")
        user_id = int(user_id)

        orders = load_data(ORDERS_FILE)
        order = next((o for o in orders if o["id"] == order_id), None)

        if order:
            order["status"] = "rejected"
            save_data(ORDERS_FILE, orders)
            send_message(user_id, f"❌ سفارش شما با شناسه {order_id} رد شد.")
            new_text = msg.get("text", "") + "\n\n❌ توسط مدیر رد شد."
            requests.post(API_URL + "editMessageText", json={
                "chat_id": chat_id,
                "message_id": message_id,
                "text": new_text
            })