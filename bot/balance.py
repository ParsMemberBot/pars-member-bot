import time
import uuid
from bot.utils import send_message, load_data, save_data, send_buttons
from bot.config import BALANCE_CHANNEL_ID, MIN_CHARGE, MAX_CHARGE

def start_balance_flow(chat_id, user_id):
    send_message(
        chat_id,
        f"💳 لطفاً مبلغ مورد نظر را **به تومان** وارد کنید.\n(حداقل: {MIN_CHARGE}، حداکثر: {MAX_CHARGE})"
    )
    save_data("data/balance_step.json", [{
        "step": "awaiting_amount",
        "user_id": user_id,
        "chat_id": chat_id,
        "timestamp": int(time.time())
    }])

def handle_balance_step(message):
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    text = message.get("text", "").strip()

    try:
        amount = int(text)
    except:
        send_message(chat_id, "❗ لطفاً مبلغ را به عدد صحیح و **به تومان** وارد کنید.")
        return

    if amount < MIN_CHARGE or amount > MAX_CHARGE:
        send_message(chat_id, f"❗ مبلغ باید **به تومان** و بین {MIN_CHARGE} تا {MAX_CHARGE} باشد.")
        return

    tx_id = str(uuid.uuid4())
    form = (
        f"💰 درخواست افزایش موجودی\n\n"
        f"👤 کاربر: {user_id}\n"
        f"💵 مبلغ: {amount} تومان\n"
        f"🆔 کد تراکنش: {tx_id}"
    )

    buttons = [[
        {"text": "✅ تایید", "callback_data": f"balance_accept:{user_id}:{amount}"},
        {"text": "❌ رد", "callback_data": f"balance_reject:{user_id}"}
    ]]

    send_buttons(BALANCE_CHANNEL_ID, form, buttons)
    send_message(chat_id, "✅ درخواست شما ثبت شد و در انتظار بررسی است.")
