import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# लॉगिंग सेटअप
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# टोकन रेंडर (Render) के Environment Variable से आएगा
TOKEN = os.getenv('BOT_TOKEN')

# आपका चैनल लिंक और ओनर आईडी
CHANNEL_LINK = "https://t.me/dragonballsuperbeerus"
OWNER_ID = 8467966989  # आपकी आईडी यहाँ सेट कर दी गई है

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 नमस्ते! मैं आपका File Hub Bot हूँ।\n\n"
        "📁 ओनर, आप मुझे कोई भी फाइल भेज सकते हैं, मैं उसे सुरक्षित कर लूँगा।",
        reply_markup=reply_markup
    )

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # ओनर चेक (सिर्फ आप ही फाइल अपलोड कर पाएंगे)
    if user_id != OWNER_ID:
        await update.message.reply_text("❌ एक्सेस डिनाइड! आप इस बॉट के मालिक (Owner) नहीं हैं।")
        return

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
            f"✅ **ओनर, फाइल स्टोर हो गई!**\n\n"
            f"📛 नाम: `{file_name}`\n"
            f"🆔 ID: `{file_id}`\n\n"
            f"इसे वापस पाने के लिए लिखें: `/get {file_id}`"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /get कमांड हर कोई इस्तेमाल कर सकता है ताकि आप फाइल शेयर कर सकें
    if not context.args:
        await update.message.reply_text("❌ कृपया फाइल ID दें। उदाहरण: `/get [ID]`")
        return

    file_id = context.args[0]
    try:
        keyboard = [[InlineKeyboardButton("Join Our Channel 📢", url=CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_document(document=file_id, reply_markup=reply_markup)
    except Exception:
        await update.message.reply_text("❌ एरर: फाइल नहीं मिली।")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: Render पर BOT_TOKEN सेट करें!")
    else:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("get", get_file))
        app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_files))
        
        print("बॉट चालू है... सिर्फ ओनर ही फाइल डाल सकता है।")
        app.run_polling()
  
