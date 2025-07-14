import time
from bot.utils import send_message, load_data, save_data
import uuid

def start_balance_flow(chat_id, user_id):
    send_message(chat_id, "🔢 لطفاً مبلغ مورد نظر برای افزایش موجودی را وارد کنید.")

def handle_balance_step(chat_id, user_id, text):
    try:
        amount = int(text)
        if amount < 1000:
            send_message(chat_id, "⚠️ مبلغ وارد شده خیلی کم است. حداقل 1000 تومان باید وارد کنید.")
            return
    except ValueError:
        send_message(chat_id, "🚫 مبلغ وارد شده نامعتبر است. فقط عدد وارد کنید.")
        return

    data = load_data("data/requests.json")
    data.setdefault("balances", [])
    
    request_id = str(uuid.uuid4())[:8]
    data["balances"].append({
        "id": request_id,
        "user_id": user_id,
        "amount": amount,
        "status": "در حال بررسی",
        "timestamp": int(time.time())
    })
    save_data("data/requests.json", data)

    send_message(chat_id, f"✅ درخواست افزایش موجودی با موفقیت ثبت شد.\nشناسه درخواست: `{request_id}`", parse_mode="Markdown")

    settings = load_data("data/settings.json")
    channel_id = settings.get("balance_channel_id")
    if channel_id:
        text = f"📥 درخواست افزایش موجودی جدید:\n\n👤 کاربر: `{user_id}`\n💰 مبلغ: {amount} تومان\n🆔 کد پیگیری: `{request_id}`"
        send_message(channel_id, text, parse_mode="Markdown")