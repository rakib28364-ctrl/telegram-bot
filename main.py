import logging
import re
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8177697588:AAHoASsVG7qxgHgx-rs0B_G3AoSzubaw0Pk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"⚡ **Power Chat ID Finder Bot** ⚡\n\n"
        f"👋 **স্বাগতম {user.first_name}!**\n"
        f"👤 **আপনার আইডি:** `{user.id}`\n\n"
        f"📌 **আমি যেসব আইডি বের করতে পারি:**\n"
        f"1️⃣ যেকোনো মেসেজ ফরোয়ার্ড করলে (User/Channel/Group ID)\n"
        f"2️⃣ যেকোনো পাবলিক ইউজারনেম (যেমন: `@username`)\n"
        f"3️⃣ যেকোনো টেলিগ্রাম লিঙ্ক (যেমন: `t.me/username`)\n"
        f"4️⃣ আমাকে কোনো গ্রুপ বা চ্যানেলে এড করলে সরাসরি আইডি দেখাবে।"
    )
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    # --- ১. ফরোয়ার্ড করা মেসেজ ডিটেকশন ---
    if msg.forward_from:
        u = msg.forward_from
        res = (
            f"👤 **ফরোয়ার্ড করা ইউজার ইনফো:**\n"
            f"• **Name:** {u.full_name}\n"
            f"• **ID:** `{u.id}`\n"
            f"• **Username:** @{u.username if u.username else 'None'}\n"
            f"• **Is Bot:** {'Yes' if u.is_bot else 'No'}"
        )
        await msg.reply_text(res, parse_mode='Markdown')
        return

    if msg.forward_from_chat:
        c = msg.forward_from_chat
        res = (
            f"📢 **ফরোয়ার্ড করা চ্যানেল/গ্রুপ ইনফো:**\n"
            f"• **Title:** {c.title}\n"
            f"• **ID:** `{c.id}`\n"
            f"• **Type:** {c.type.capitalize()}\n"
            f"• **Username:** @{c.username if c.username else 'None'}"
        )
        await msg.reply_text(res, parse_mode='Markdown')
        return

    # --- ২. ইউজারনেম বা লিঙ্ক প্রসেসিং ---
    text = msg.text
    if text:
        # লিঙ্ক থেকে ইউজারনেম ফিল্টার করা
        extracted = re.findall(r'(?:https?://)?(?:www\.)?t(?:elegram)?\.(?:me|dog)/([a-zA-Z0-9_]+)', text)
        target = f"@{extracted[0]}" if extracted else text.strip()

        if target.startswith("@") and len(target) > 1:
            try:
                chat = await context.bot.get_chat(target)
                title = chat.title if chat.title else chat.first_name
                res = (
                    f"🔍 **ইনফরমেশন পাওয়া গেছে:**\n\n"
                    f"• **Title/Name:** {title}\n"
                    f"• **Chat ID:** `{chat.id}`\n"
                    f"• **Type:** {chat.type.capitalize()}\n"
                    f"• **Username:** @{chat.username if chat.username else 'None'}"
                )
                await msg.reply_text(res, parse_mode='Markdown')
                return
            except Exception:
                await msg.reply_text(
                    "❌ **আইডি পাওয়া যায়নি!**\n"
                    "ইউজারনেম বা লিঙ্কটি সঠিক এবং পাবলিক কি না নিশ্চিত হয়ে আবার চেষ্টা করুন।",
                    parse_mode='Markdown'
                )
                return

    # --- ৩. সাধারণ মেসেজ হলে প্রেরকের নিজের ID ---
    await msg.reply_text(
        f"🆔 **Chat ID:** `{msg.chat.id}`\n"
        f"👤 **User ID:** `{msg.from_user.id}`",
        parse_mode='Markdown'
    )

# --- ৪. গ্রুপ বা চ্যানেলে এড হলে আইডি সেন্ড করা ---
async def handle_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=f"⚙️ **নতুন আড্ডা/চ্যানেলে বটের উপস্থিতি:**\n\n📌 **{chat.type.capitalize()} Title:** {chat.title}\n🆔 **ID:** `{chat.id}`",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_bot_added))
    app.add_handler(MessageHandler(filters.ALL, handle_all_messages))

    app.run_polling()
        
