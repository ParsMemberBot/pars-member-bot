import json
import time
from bot.utils import load_data, save_data, send_message

def handle_store(chat_id, user_id):
    settings = load_data("data/settings.json")
    categories = settings.get("categories", [])

    if not categories:
        send_message(chat_id, "هیچ دسته‌بندی‌ای در فروشگاه ثبت نشده است.")
        return

    buttons = [[{"text": cat["title"], "callback_data": f"cat_{cat['id']}"}] for cat in categories]
    buttons.append([{"text": "بازگشت", "callback_data": "back_to_menu"}])
    send_message(chat_id, "لطفاً یک دسته را انتخاب کنید:", {"keyboard": buttons, "resize_keyboard": True})

def process_category_selection(chat_id, user_id, category_id):
    settings = load_data("data/settings.json")
    products = [p for p in settings.get("products", []) if p["category_id"] == category_id]

    if not products:
        send_message(chat_id, "در این دسته محصولی ثبت نشده است.")
        return

    buttons = []
    for product in products:
        title = product["title"]
        price = product["price"]
        btn_text = f"{title} - {price} تومان"
        buttons.append([{"text": btn_text, "callback_data": f"product_{product['id']}"}])

    buttons.append([{"text": "بازگشت", "callback_data": "store"}])
    send_message(chat_id, "یک محصول انتخاب کنید:", {"keyboard": buttons, "resize_keyboard": True})

def process_product_selection(chat_id, user_id, product_id):
    users = load_data("data/users.json")
    user = users.get(str(user_id), {})
    user["state"] = f"awaiting_quantity_{product_id}"
    users[str(user_id)] = user
    save_data("data/users.json", users)
    send_message(chat_id, "چه تعداد از این محصول می‌خواهید سفارش دهید؟")

def process_quantity_input(chat_id, user_id, quantity_text):
    users = load_data("data/users.json")
    settings = load_data("data/settings.json")
    user = users.get(str(user_id), {})

    state = user.get("state", "")
    if not state.startswith("awaiting_quantity_"):
        return

    try:
        quantity = int(quantity_text)
    except:
        send_message(chat_id, "لطفاً تعداد را به‌صورت عدد وارد کنید.")
        return

    product_id = state.replace("awaiting_quantity_", "")
    product = next((p for p in settings.get("products", []) if p["id"] == product_id), None)
    if not product:
        send_message(chat_id, "محصول یافت نشد.")
        return

    min_q = product.get("min", 1)
    max_q = product.get("max", 1000)
    if min_q and quantity < min_q:
        send_message(chat_id, f"حداقل تعداد سفارش برای این محصول {min_q} است.")
        return
    if max_q and quantity > max_q:
        send_message(chat_id, f"حداکثر تعداد سفارش برای این محصول {max_q} است.")
        return

    user["state"] = f"awaiting_description_{product_id}_{quantity}"
    users[str(user_id)] = user
    save_data("data/users.json", users)
    send_message(chat_id, "توضیحات سفارش را وارد کنید (اختیاری است). اگر توضیحی ندارید، فقط عدد 0 را بفرستید.")

def process_description_input(chat_id, user_id, text):
    users = load_data("data/users.json")
    orders = load_data("data/orders.json")
    settings = load_data("data/settings.json")
    user = users.get(str(user_id), {})
    state = user.get("state", "")

    if not state.startswith("awaiting_description_"):
        return

    _, product_id, quantity = state.split("_")[2:]
    quantity = int(quantity)
    description = "" if text.strip() == "0" else text.strip()
    product = next((p for p in settings.get("products", []) if p["id"] == product_id), None)

    if not product:
        send_message(chat_id, "محصول مورد نظر یافت نشد.")
        return

    timestamp = int(time.time())
    order_id = f"{user_id}_{timestamp}"

    new_order = {
        "id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "description": description,
        "status": "pending"
    }
    orders[order_id] = new_order
    save_data("data/orders.json", orders)

    user["state"] = ""
    users[str(user_id)] = user
    save_data("data/users.json", users)

    # ارسال به کانال فرم سفارش
    channel_id = settings.get("order_channel_id")
    if channel_id:
        order_text = f"""📦 سفارش جدید ثبت شد:

🆔 آیدی سفارش: {order_id}
📌 محصول: {product['title']}
🔢 تعداد: {quantity}
👤 کاربر: {user_id}
📝 توضیح: {description or 'ندارد'}"""
        send_message(channel_id, order_text)

    send_message(chat_id, "✅ سفارش شما با موفقیت ثبت شد و در حال بررسی است.")
