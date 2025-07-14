import time
import uuid
from bot.utils import send_message, send_buttons, load_data, save_data
from bot.config import ORDER_CHANNEL_ID

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

        # متن سفارش
        order_text = (
            f"📦 سفارش جدید:\n\n"
            f"👤 کاربر: {step_data['order']['user_id']}\n"
            f"🗂 دسته: {step_data['order']['category']}\n"
            f"📦 محصول: {step_data['order']['product']}\n"
            f"📝 توضیحات: {step_data['order']['details']}\n"
            f"🆔 شناسه سفارش: {step_data['order']['id']}\n"
            f"⏳ وضعیت: در حال بررسی"
        )

        # دکمه تایید/رد
        buttons = [
            [
                {"text": "✅ تایید سفارش", "callback_data": f"order_accept:{step_data['order']['user_id']}:{step_data['order']['id']}"},
                {"text": "❌ رد سفارش", "callback_data": f"order_reject:{step_data['order']['user_id']}:{step_data['order']['id']}"}
            ]
        ]

        send_buttons(ORDER_CHANNEL_ID, order_text, buttons)

        send_message(chat_id, "✅ سفارش شما با موفقیت ثبت شد. منتظر تایید بمانید.")
        return None
