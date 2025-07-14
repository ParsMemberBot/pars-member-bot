import time
import uuid
from bot.utils import send_message, load_data, save_data

def start_balance_flow(chat_id, user_id):
    send_message(chat_id, "🔢 لطفاً مبلغ مورد نظر برای افزایش موجودی را وارد کنید.")
    state = load_data("data/state.json")
    state[str(user_id)] = {"step": "enter_balance_amount"}
    save_data("data/state.json", state)

def handle_balance_step(chat_id, user_id, text):
    if not text.isdigit():
        send_message(chat_id, "🚫 مبلغ وارد شده نامعتبر است. فقط عدد وارد کنید.")
        return

    amount = int(text)
    if amount < 1000:
        send_message(chat_id, "⚠️ مبلغ وارد شده خیلی کم است. حداقل 1000 تومان باید وارد کنید.")
        return

    # تولید شناسه یکتا برای درخواست
    request_id = str(uuid.uuid4())[:8]

    # ذخیره اطلاعات درخواست
    balances = load_data("data/balances.json")
    balances[request_id] = {
        "user_id": user_id,
        "chat_id": chat_id,
        "amount": amount,
        "status": "در حال بررسی",
        "time": time.time()
    }
    save_data("data/balances.json", balances)

    send_message(chat_id, f"✅ درخواست افزایش موجودی با موفقیت ثبت شد.\nشناسه درخواست: `{request_id}`", parse_mode="Markdown")

    # ارسال پیام به کانال فرم افزایش موجودی
    text = f"""
📥 درخواست افزایش موجودی جدید

👤 کاربر: `{user_id}`
💰 مبلغ: {amount:,} تومان
🆔 شناسه درخواست: `{request_id}`

⏳ وضعیت: در حال بررسی
    """.strip()

    channel_id = 5871189664  # آیدی عددی کانال فرم افزایش موجودی
    if text:
        send_message(channel_id, text, parse_mode="Markdown")
    else:
        print("⛔ پیام فرم افزایش موجودی خالی بود و ارسال نشد.")
