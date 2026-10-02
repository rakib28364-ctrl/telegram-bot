from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8177697588:AAHoASsVG7qxgHgx-rs0B_G3AoSzubaw0Pk"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📞 Make a Call", "📹 Call Recordings"],
        ["💰 My Balance", "🎁 Daily Bonus"],
        ["👥 Refer & Earn", "❓ Help"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🤖 Welcome to Call Bot!\nনিচের মেনু থেকে অপশন সিলেক্ট করুন।",
        reply_markup=reply_markup,
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()
  
