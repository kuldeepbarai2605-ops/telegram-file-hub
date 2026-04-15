import logging
import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Forbidden

# लॉगिंग
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = "@dragonballsuperbeerus"
CHANNEL_LINK = "https://t.me/dragonballsuperbeerus"
GROUP_LINK = "https://t.me/dragonballsuperbeerus1"
OWNER_ID = 8467966989 
ADMINS = [8467966989]

# --- वेलकम फोटो लिंक ---
# यहाँ अपनी फोटो का डायरेक्ट लिंक डालें (जैसे Imgur या किसी टेलीग्राम फाइल का लिंक)
WELCOME_PHOTO = "https://तेरी_फोटो_का_लिंक.jpg" 

# डेटाबेस सेटअप
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
conn.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

async def is_user_joined(context, user_id):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status not in ['left', 'kicked']
    except Exception: return False

# --- वेलकम मैसेज (फोटो के साथ) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    add_user(user_id)
    
    keyboard = [
        [InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Join Group 💬", url=GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🔥 **Welcome to Dragon Ball Super Beerus!** 🔥\n\n"
        "नमस्ते! मैं आपका फाइल हब बॉट हूँ। यहाँ आपको बेहतरीन कंटेंट मिलेगा।\n\n"
        "📢 आगे बढ़ने के लिए नीचे दिए गए बटन से चैनल और ग्रुप जॉइन करें।"
    )

    try:
        # फोटो के साथ मैसेज भेजना
        await update.message.reply_photo(
            photo=WELCOME_PHOTO,
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception:
        # अगर फोटो लोड न हो, तो सिर्फ टेक्स्ट भेजें
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- ब्रॉडकास्ट फीचर ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID: return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ किसी मैसेज को 'Reply' करके `/broadcast` लिखें।")
        return

    reply_msg = update.message.reply_to_message
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    await update.message.reply_text(f"🚀 {len(users)} यूजर्स को ब्रॉडकास्ट शुरू...")
    
    for user in users:
        try:
            await context.bot.copy_message(chat_id=user[0], from_chat_id=reply_msg.chat_id, message_id=reply_msg.message_id)
        except Exception: pass
    
    await update.message.reply_text("✅ ब्रॉडकास्ट सफल!")

# बाकी के फंक्शन (get_file और handle_files) पहले जैसे ही रहेंगे...
# [यहाँ पिछला handle_files और get_file कोड जोड़ें]

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    # ... बाकी हैंडलर्स
    app.run_polling()
