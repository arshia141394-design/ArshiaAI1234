import requests

from rubka import Robot
from rubka.asynco import Message

# =========================
# تنظیمات
# =========================

BOT_TOKEN =  "BICAGB0SZXZSXDGXLSORLPNLLOBVHTNXYBPTWSBMROFLETWWEOHOPPWMLBAOKALG"

OPENROUTER_API_KEY =  "sk-or-v1-c3b...360"


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# =========================
# ساخت ربات
# =========================

bot = Robot(BOT_TOKEN)


# =========================
# اتصال به هوش مصنوعی
# =========================

def ask_ai(question):

    response = requests.post(
        OPENROUTER_URL,

        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },

        json={
            "model": "openrouter/free",

            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },

        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


# =========================
# دریافت پیام‌ها
# =========================

@bot.on_message()
async def commands(client, message):

    if not message.text:
        return

    text = message.text.strip()

    if not text:
        return


    # =====================
    # دستور شروع
    # =====================

    if text == "/start":

        await message.reply(
            "⭐ Arshia StarAI\n\n"
            "سلام! من Arshia StarAI هستم 🤖\n"
            "به دنیای هوش مصنوعی خوش اومدی 🌟\n\n"

            "دستورها:\n\n"

            "🧠 سوال - سوالت\n"
            "🔎 جستجو - عبارت موردنظر\n"
            "🌍 ترجمه - متن"
        )


    # =====================
    # سوال هوش مصنوعی
    # =====================

    elif text.startswith("سوال"):

        question = text.replace("سوال", "", 1).strip()

        if question.startswith("-"):
            question = question[1:].strip()

        if not question:

            await message.reply(
                "❓ لطفاً بعد از «سوال» پرسشت را بنویس."
            )

            return


        try:

            await message.reply("🤖 دارم فکر می‌کنم...")

            answer = ask_ai(question)

            await message.reply(
                f"🧠 پاسخ:\n\n{answer}"
            )

        except Exception as e:

            await message.reply(
                f"❌ خطا در اتصال به هوش مصنوعی:\n\n{e}"
            )


    # =====================
    # جستجو
    # =====================

    elif text.startswith("جستجو"):

        query = text.replace("جستجو", "", 1).strip()

        if not query:

            await message.reply(
                "🔎 لطفاً عبارت موردنظر را وارد کن."
            )

            return

        await message.reply(
            f"🔎 جستجو برای:\n{query}\n\n"
            "بخش جستجو را در مرحله بعد کامل می‌کنیم."
        )


    # =====================
    # ترجمه
    # =====================

    elif text.startswith("ترجمه"):

        sentence = text.replace("ترجمه", "", 1).strip()

        if not sentence:

            await message.reply(
                "🌍 لطفاً متنی که می‌خواهی ترجمه شود را بنویس."
            )

            return

        await message.reply(
            f"🌍 متن دریافت شد:\n\n{sentence}\n\n"
            "بخش ترجمه را در مرحله بعد اضافه می‌کنیم."
        )


    # =====================
    # دستور نامعتبر
    # =====================

    else:

        await message.reply(
            "❓ دستور نامعتبر است.\n\n"
            "برای شروع /start را بفرست."
        )


# =========================
# اجرای ربات
# =========================

bot.run()