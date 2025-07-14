import time
from bot.utils import send_message, load_data, save_data
from bot.config import ORDER_CHANNEL_ID
import uuid

def start_order_flow(chat_id, user_id):
    step_data = {
        "step": "awaiting_category",
        "order": {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "chat_id": chat_id,
            "status": "در حال بررسی",
            "timestamp": int(time.time())
        }
    }

    orders = load_data("data/orders.json")
    orders.append(step_data["order"])
    save_data("data/orders.json", orders)

    send_message(chat_id, "لطفاً دسته‌بندی محصول را وارد کنید:")
    return step_data

def handle_order_step(message, step_data):
    text = message.get("text", "").strip()
    chat_id = message["chat"]["id"]

    if step_data["step"] == "awaiting_category":
        step_data["order"]["category"] = text
        step_data["step"] = "awaiting_product"
        send_message(chat_id, "نام محصول مورد نظر را وارد کنید:")
        return step_data

    elif step_data["step"] == "awaiting_product":
        step_data["order"]["product"] = text
        step_data["step"] = "awaiting_details"
        send_message(chat_id, "توضیحات سفارش را وارد کنید:")
        return step_data

    elif step_data["step"] == "awaiting_details":
        step_data["order"]["details"] = text
        step_data["step"] = "completed"

        orders = load_data("data/orders.json")
        for order in orders:
            if order["id"] == step_data["order"]["id"]:
                order.update(step_data["order"])
                break
        save_data("data/orders.json", orders)

        # ارسال به کانال سفارشات
        text = f"📦 سفارش جدید:\n\n"
        text += f"👤 کاربر: {step_data['order']['user_id']}\n"
        text += f"🗂 دسته: {step_data['order']['category']}\n"
        text += f"📦 محصول: {step_data['order']['product']}\n"
        text += f"📝 توضیحات: {step_data['order']['details']}\n"
        text += f"⏳ وضعیت: در حال بررسی"

        send_message(ORDER_CHANNEL_ID, text)

        send_message(chat_id, "✅ سفارش شما با موفقیت ثبت شد. منتظر تایید بمانید.")
        return None
