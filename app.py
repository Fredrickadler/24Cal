import random
import os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیمات
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# لود لیست BIP-39
with open("bip39_wordlist.txt", "r") as f:
    BIP39_WORDLIST = [line.strip() for line in f]

# اپ Flask برای Render
app = Flask(__name__)

# تولید عبارت بازیابی
def generate_seed_phrase(word_count):
    return " ".join(random.sample(BIP39_WORDLIST, word_count))

# پیام خوش‌آمدگویی با دکمه‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📜 ۱۲ کلمه", callback_data="12"),
            InlineKeyboardButton("📜 ۲۴ کلمه", callback_data="24")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 به ربات تولید عبارت بازیابی خوش اومدید!\n"
        "لطفاً تعداد کلمات مورد نظر رو انتخاب کنید:\n"
        "⚠️ این عبارات برای تست کیف‌پول‌های خودتون استفاده بشن!",
        reply_markup=reply_markup
    )

# مدیریت کلیک روی دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    word_count = int(query.data)
    seed_phrase = generate_seed_phrase(word_count)
    
    await query.message.reply_text(
        f"🔑 عبارت بازیابی {word_count} کلمه‌ای:\n```\n{seed_phrase}\n```\n"
        "✅ این عبارت با استاندارد BIP-39 سازگاره و تو کیف‌پول‌هایی مثل متامسک، تراست والت یا لجر کار می‌کنه.\n"
        "⚠️ هرگز تو محیط ناامن ذخیره نکنید!",
        parse_mode="Markdown"
    )

# ربات تلگرام
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# رابط Flask برای Render
@app.route("/")
def index():
    return "Telegram Bot is running!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=main, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
