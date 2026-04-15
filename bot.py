import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# लॉगिंग सेटअप
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# टोकन रेंडर के Environment Variable से आएगा
TOKEN = os.getenv('BOT_TOKEN')

# आपका चैनल लिंक यहाँ फिक्स कर दिया गया है
CHANNEL_LINK = "https://t.me/dragonballsuperbeerus"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # चैनल जॉइन करने के लिए बटन
    keyboard = [[InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 नमस्ते! मैं आपका File Hub Bot हूँ।\n\n"
        "📁 मुझे कोई भी फाइल भेजें, मैं उसे सुरक्षित कर लूँगा और आपको एक ID दूँगा।\n"
        "उस ID का उपयोग करके आप कभी भी फाइल वापस पा सकते हैं।",
        reply_markup=reply_markup
    )

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = ""
    file_name = "File"

    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
    elif update.message.video:
        file_id = update.message.video.file_id
        file_name = "Video"
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_name = "Photo"

    if file_id:
        response = (
            f"✅ **फाइल स्टोर हो गई!**\n\n"
            f"📛 नाम: `{file_name}`\n"
            f"🆔 ID: `{file_id}`\n\n"
            f"फाइल वापस पाने के लिए लिखें: `/get {file_id}`"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ कृपया फाइल ID दें। उदाहरण: `/get [ID]`")
        return

    file_id = context.args[0]
    try:
        # फाइल भेजते समय भी चैनल का बटन दिखेगा
        keyboard = [[InlineKeyboardButton("More Content 📢", url=CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_document(document=file_id, reply_markup=reply_markup)
    except Exception:
        await update.message.reply_text("❌ एरर: फाइल नहीं मिली। कृपया सही ID चेक करें।")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: Render पर BOT_TOKEN सेट नहीं किया गया है!")
    else:
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("get", get_file))
        app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_files))
        
        print("बॉट चालू है और आपके चैनल से जुड़ा है...")
        app.run_polling()
