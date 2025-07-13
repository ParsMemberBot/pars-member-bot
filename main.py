from flask import Flask
from threading import Thread
from keep_alive import keep_alive
import requests, json, time, os

TOKEN = "1010361809:ZmiQrwFd9PDofNsoFFiGl67kG6Sk9znxqoLHZi27"
ADMIN_ID = "508276871"
FORM_ORDER_CHANNEL = "-1002224018860"
FORM_CHARGE_CHANNEL = "-1001941542064"

API = f"https://tapi.bale.ai/bot{TOKEN}"
USERS_FILE = "data/users.json"
ORDERS_FILE = "data/orders.json"

users = {}
orders = {}

# --- Utility Functions ---
def load_data():
    global users, orders
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)

def save_data():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def send_message(chat_id, text, buttons=None):
    data = {"chat_id": chat_id, "text": text}
    if buttons:
        data["reply_markup"] = {"inline_keyboard": buttons}
    requests.post(f"{API}/sendMessage", json=data)

def forward_to_channel(channel_id, message_text, buttons=None):
    data = {"chat_id": channel_id, "text": message_text}
    if buttons:
        data["reply_markup"] = {"inline_keyboard": buttons}
    return requests.post(f"{API}/sendMessage", json=data)

# --- Command Handlers ---
def handle_start(user_id, chat_id):
    if user_id not in users:
        users[user_id] = {"balance": 0, "orders": [], "warns": 0}
        save_data()
    send_message(chat_id,
        "سلام! به ربات خوش آمدید 🎉\n\n"
        "دستورات:\n"
        "/balance → موجودی\n"
        "/charge → افزایش موجودی\n"
        "/order → ثبت سفارش\n"
        "/myorders → سفارشات من\n"
        "/support → پشتیبانی")

def handle_balance(user_id, chat_id):
    balance = users.get(user_id, {}).get("balance", 0)
    send_message(chat_id, f"💰 موجودی شما: {balance} تومان")

def handle_charge(user_id, chat_id):
    users[user_id]["awaiting_charge"] = True
    save_data()
    send_message(chat_id, "لطفاً مبلغ مورد نظر را به تومان وارد کنید (حداقل 10000).")

def handle_order(user_id, chat_id):
    users[user_id]["awaiting_order"] = True
    save_data()
    send_message(chat_id, "نوع سفارش را بنویسید. مثلا:\nممبر تلگرام 100 عدد")

def handle_myorders(user_id, chat_id):
    orders_list = users[user_id].get("orders", [])
    if not orders_list:
        send_message(chat_id, "📦 سفارشی ثبت نکرده‌اید.")
        return
    msg = "📋 سفارشات شما:\n"
    for o in orders_list:
        status = orders.get(str(o), {}).get("status", "نامشخص")
        msg += f"▪️ سفارش #{o} - وضعیت: {status}\n"
    send_message(chat_id, msg)

def handle_support(chat_id):
    send_message(chat_id, "برای پشتیبانی با آیدی زیر در ارتباط باشید:\n@CyrusParsy",
                 [[{"text": "🔗 ارتباط با پشتیبانی", "url": "https://ble.ir/CyrusParsy"}]])

# --- Polling and Main Handler ---
def process_update(update):
    if "message" not in update: return
    msg = update["message"]
    chat_id = str(msg["chat"]["id"])
    user_id = chat_id
    text = msg.get("text", "")

    if chat_id.startswith("-"): return  # جلوگیری از پاسخ به کانال یا گروه

    if user_id not in users:
        users[user_id] = {"balance": 0, "orders": [], "warns": 0}
        save_data()

    if text == "/start":
        handle_start(user_id, chat_id)
    elif text == "/balance":
        handle_balance(user_id, chat_id)
    elif text == "/charge":
        handle_charge(user_id, chat_id)
    elif text == "/order":
        handle_order(user_id, chat_id)
    elif text == "/myorders":
        handle_myorders(user_id, chat_id)
    elif text == "/support":
        handle_support(chat_id)
    elif users[user_id].get("awaiting_charge"):
        try:
            amount = int(text)
            if amount >= 10000:
                users[user_id]["awaiting_charge"] = False
                form = f"🔋 درخواسـت افزایش موجودی\n\n👤 کاربر: {user_id}\n💰 مبلغ: {amount} تومان"
                forward_to_channel(FORM_CHARGE_CHANNEL, form,
                    [[{"text": "✅ تایید", "callback_data": f"approve_charge_{user_id}_{amount}"},
                      {"text": "❌ لغو", "callback_data": f"cancel_charge_{user_id}"}]])
                send_message(chat_id, "درخواست شما ارسال شد ✅\nمنتظر تایید توسط مدیریت باشید.")
            else:
                send_message(chat_id, "حداقل مبلغ 10000 تومان است.")
        except:
            send_message(chat_id, "لطفاً مبلغ را به عدد صحیح وارد کنید.")
        save_data()
    elif users[user_id].get("awaiting_order"):
        users[user_id]["awaiting_order"] = False
        order_id = len(orders) + 1
        orders[str(order_id)] = {"user_id": user_id, "desc": text, "status": "در حال انجام"}
        users[user_id]["orders"].append(order_id)
        save_data()
        form = f"🛒 سفارش جدید ثبت شد:\n\n👤 کاربر: {user_id}\n📝 توضیح: {text}\n🆔 سفارش: {order_id}"
        forward_to_channel(FORM_ORDER_CHANNEL, form,
            [[{"text": "✅ تایید", "callback_data": f"approve_order_{user_id}_{order_id}"},
              {"text": "❌ لغو", "callback_data": f"cancel_order_{user_id}_{order_id}"}]])
        send_message(chat_id, "✅ سفارش شما ثبت شد و در صف بررسی است.")
    else:
        send_message(chat_id, "دستور ناشناس است. لطفاً از منو استفاده کنید.")

# --- Bot Polling ---
def polling():
    offset = None
    while True:
        try:
            res = requests.get(f"{API}/getUpdates", params={"offset": offset})
            updates = res.json().get("result", [])
            for u in updates:
                offset = u["update_id"] + 1
                process_update(u)
        except Exception as e:
            print("خطا:", e)
        time.sleep(0.07)

# --- Start App ---
keep_alive()
load_data()
print("🤖 ربات در حال اجراست...")
Thread(target=polling).start()
