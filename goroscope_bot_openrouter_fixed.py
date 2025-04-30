from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests


TELEGRAM_TOKEN = "7662648491:AAFwaIR9q3Fue65cRKB_4vToUfC_5RjARkM"
OPENROUTER_API_KEY = "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"

zodiacs = [
    "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
    "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
]

keyboard = ReplyKeyboardMarkup([[z] for z in zodiacs], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-гороскоп. Выбери свой знак зодиака:",
        reply_markup=keyboard
    )

async def get_horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().capitalize()

    if user_input not in zodiacs:
        await update.message.reply_text("Пожалуйста, выбери знак зодиака из списка.")
        return

    prompt = f"Напиши позитивный, вдохновляющий гороскоп на сегодня для знака зодиака {user_input}."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
         "model": "anthropic/claude-2",
        "max_tokens": 200,  # добавляем ограничение
        "messages": [
        {"role": "user", "content": prompt}
        ]
}

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        data = response.json()
        if "choices" in data:
            horoscope = data["choices"][0]["message"]["content"]
            await update.message.reply_text(horoscope)
        else:
            await update.message.reply_text(f"⚠️ Ответ не содержит 'choices':\n{data}")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка разбора ответа:\n{e}")

print("✅ Бот запущен с OpenRouter. Жду сообщений...")
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_horoscope))
app.run_polling()
