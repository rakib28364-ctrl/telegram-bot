import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8177697588:AAHoASsVG7qxgHgx-rs0B_G3AoSzubaw0Pk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"👋 **স্বাগতম {user.first_name}!**\n\n"
        f"🆔 **আপনার Chat ID:** `{user.id}`\n\n"
        f"💡 **যা যা করতে পারবেন:**\n"
        f"• যেকোনো মেসেজ ফরোয়ার্ড করলে তার মূল আইডি দেখাবে।\n"
        f"• কোনো ইউজারনেম (যেমন: `@username`) লিখে পাঠালে তার আইডি দেখাবে।\n"
        f"• আমাকে কোনো গ্রুপ বা চ্যানেলে এড করলে সেই গ্রুপ/চ্যানেলের আইডি দেখাবে।"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # Forwarded message check
    if message.forward_from:
        forwarded_user = message.forward_from
        await message.reply_text(
            f"👤 **ফরোয়ার্ড করা ইউজার ইনফো:**\n"
            f"• **Name:** {forwarded_user.full_name}\n"
            f"• **User ID:** `{forwarded_user.id}`\n"
            f"• **Username:** @{forwarded_user.username if forwarded_user.username else 'N/A'}",
            parse_mode='Markdown'
        )
        return
    elif message.forward_from_chat:
        forwarded_chat = message.forward_from_chat
        await message.reply_text(
            f"📢 **ফরোয়ার্ড করা চ্যানেল/গ্রুপ ইনফো:**\n"
            f"• **Title:** {forwarded_chat.title}\n"
            f"• **ID:** `{forwarded_chat.id}`\n"
            f"• **Type:** {forwarded_chat.type.capitalize()}\n"
            f"• **Username:** @{forwarded_chat.username if forwarded_chat.username else 'N/A'}",
            parse_mode='Markdown'
        )
        return

    # Text username check
    text = message.text
    if text and text.startswith("@"):
        username = text.strip()
        try:
            chat = await context.bot.get_chat(username)
            info = (
                f"🔍 **ইনফরমেশন:**\n"
                f"• **Title/Name:** {chat.title if chat.title else chat.first_name}\n"
                f"• **ID:** `{chat.id}`\n"
                f"• **Type:** {chat.type.capitalize()}\n"
                f"• **Username:** @{chat.username}"
            )
            await message.reply_text(info, parse_mode='Markdown')
        except Exception:
            await message.reply_text("❌ আইডি পাওয়া যায়নি। ইউজারনেমটি সঠিক কি না এবং অ্যাকাউন্ট/চ্যানেলটি পাবলিক কি না চেক করুন।")
        return

    # Normal user ID echo
    await message.reply_text(f"🆔 **আপনার Chat ID:** `{message.chat.id}`", parse_mode='Markdown')

# Handle bot being added to group or channel
async def handle_new_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=f"🎉 **ধন্যবাদ আমাকে যুক্ত করার জন্য!**\n\n📌 **এই {chat.type.capitalize()}-এর ID:** `{chat.id}`",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat))
    app.add_handler(MessageHandler(filters.TEXT | filters.FORWARDED, handle_message))

    app.run_polling()
            
