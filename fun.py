import random
from utils import send_message, chatgpt_response

jokes = [
    "🤣 چرا برنامه‌نویسا هیچ‌وقت گم نمی‌شن؟ چون همیشه یه مسیر برگشتی دارن!",
    "😆 طرف رفته پیش روانشناس، گفته چرا با پایتون خواب می‌بینم؟ گفته چون async داری!",
    "😂 فرق مهندس کامپیوتر با جادوگر چیه؟ جادوگر جادو می‌کنه، مهندس باگ می‌گیره!"
]

fortunes = [
    "🔮 آینده روشنی در انتظارت هست.",
    "💫 به زودی خبری خوشحال‌کننده می‌رسه.",
    "🌟 نیت کن... بهش می‌رسی اگر تلاش کنی.",
    "🍀 شانس در خونه‌ت رو می‌زنه. دریابش!"
]

def handle_fun_commands(message):
    text = message.get("text", "")
    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]

    if text == "جوک":
        joke = random.choice(jokes)
        send_message(chat_id, joke)

    elif text == "فال":
        fortune = random.choice(fortunes)
        send_message(chat_id, fortune)

    elif text.startswith("/ai") or text.startswith("هوش مصنوعی") or text.startswith("ربات"):
        prompt = text.replace("/ai", "").replace("هوش مصنوعی", "").replace("ربات", "").strip()
        if not prompt:
            send_message(chat_id, "❗️لطفاً بعد از دستور، سوال یا متن خود را بنویسید.")
        else:
            response = chatgpt_response(prompt)
            send_message(chat_id, response)
