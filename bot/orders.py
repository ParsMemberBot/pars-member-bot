
import json
import time
import uuid
from bot.utils import send_message, load_data, save_data
from config import ORDER_CHANNEL_ID

ORDERS_FILE = "data/orders.json"

def create_order(user_id, category, product, quantity, price):
    orders = load_data(ORDERS_FILE)
    order_id = str(uuid.uuid4())[:8]
    order = {
        "id": order_id,
        "user_id": user_id,
        "category": category,
        "product": product,
        "quantity": quantity,
        "price": price,
        "status": "در حال بررسی",
        "timestamp": int(time.time())
    }
    orders.append(order)
    save_data(ORDERS_FILE, orders)
    return order

def get_user_orders(user_id):
    orders = load_data(ORDERS_FILE)
    return [o for o in orders if o["user_id"] == user_id]

def get_order_by_id(order_id):
    orders = load_data(ORDERS_FILE)
    for o in orders:
        if o["id"] == order_id:
            return o
    return None

def update_order_status(order_id, new_status):
    orders = load_data(ORDERS_FILE)
    for o in orders:
        if o["id"] == order_id:
            o["status"] = new_status
            save_data(ORDERS_FILE, orders)
            return True
    return False

def send_order_to_channel(order, bot):
    msg = (
        f"🛒 سفارش جدید ثبت شد\n\n"
        f"🆔 کد سفارش: {order['id']}\n"
        f"👤 آیدی عددی کاربر: {order['user_id']}\n"
        f"📦 دسته: {order['category']}\n"
        f"🛍️ محصول: {order['product']}\n"
        f"🔢 تعداد: {order['quantity']}\n"
        f"💰 مبلغ: {order['price']} تومان\n\n"
        f"📌 برای تأیید یا رد از پنل استفاده کنید."
    )
    bot.send_message(chat_id=ORDER_CHANNEL_ID, text=msg)
