import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

# लॉगिंग
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# टोकन Render के Environment Variables से आएगा
TOKEN = os.getenv('BOT_TOKEN')

# --- सेटिंग्स ---
CHANNEL_ID = "@dragonballsuperbeerus"
CHANNEL_LINK = "https://t.me/dragonballsuperbeerus"
GROUP_LINK = "https://t.me/dragonballsuperbeerus1"
OWNER_ID = 8467966989 
ADMINS = [8467966989] # यहाँ और IDs जोड़ सकते हैं

async def is_user_joined(context, user_id):
    try:
        # चैनल की सदस्यता चेक करें
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status not in ['left', 'kicked']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # चैनल और ग्रुप दोनों के बटन
    keyboard = [
        [InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Join Group 💬", url=GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 नमस्ते! मैं File Hub Bot हूँ।\n\n"
        "🛑 फाइल एक्सेस करने के लिए नीचे दिए गए बटन से चैनल और ग्रुप जॉइन करें।",
        reply_markup=reply_markup
    )

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in ADMINS:
        await update.message.reply_text("❌ केवल ओनर/एडमिन ही फाइल अपलोड कर सकते हैं।")
        return

    file_id = ""
    file_name = "File"
    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
    elif update.message.video:
        file_id = update.message.video.file_id
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id

    if file_id:
        await update.message.reply_text(
            f"✅ **फाइल सुरक्षित हो गई!**\n\n🆔 ID: `{file_id}`\n\n"
            f"शेयर करने के लिए: `/get {file_id}`", 
            parse_mode='Markdown'
        )

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # Force Join Check (सिर्फ साधारण यूजर्स के लिए)
    if user_id not in ADMINS:
        joined = await is_user_joined(context, user_id)
        if not joined:
            keyboard = [
                [InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)],
                [InlineKeyboardButton("Join Group 💬", url=GROUP_LINK)]
            ]
            await update.message.reply_text(
                "🛑 रुकिए! आपने अभी तक हमारा चैनल जॉइन नहीं किया है।\nफाइल पाने के लिए जॉइन करें:", 
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

    if not context.args:
        await update.message.reply_text("❌ कृपया फाइल ID दें।")
        return

    file_id = context.args[0]
    try:
        await update.message.reply_document(document=file_id)
    except Exception:
        await update.message.reply_text("❌ फाइल नहीं मिली या ID गलत है।")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: BOT_TOKEN Not Found!")
    else:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("get", get_file))
        app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_files))
        
        print("बॉट लाइव है...")
        app.run_polling()
