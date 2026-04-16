import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from threading import Thread
import json

# ---------- CONFIG ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8406116569:AAHHyPYjaZtUnloWRkXZWDSzSyMpaOL7WX0")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://YOUR_HOSTED_URL/daidi_miniapp.html")  # ← change this

if not BOT_TOKEN:
    print("Error: BOT_TOKEN not set.")
    exit(1)

def heartbeat():
    import time
    while True:
        print("💓 Bot alive")
        time.sleep(300)

Thread(target=heartbeat, daemon=True).start()

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "🃏 Open Dai Di Tracker",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Out of cash? Jerica and Aloysius gotchu!\n"
        "I'm your Dai Di Money Tracker Bot 💰\n\n"
        "Tap the button below to open the tracker 👇",
        reply_markup=reply_markup
    )

# ---------- Handle Mini App data ----------
# The Mini App sends data via sendData() which comes in as a web_app_data message
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_str = update.effective_message.web_app_data.data
    try:
        data = json.loads(data_str)
        action = data.get("action", "update")
        scores = data.get("scores", "")
        round_num = data.get("round", 0)

        if action == "Game ended":
            await update.message.reply_text(
                f"🏁 Game Over!\n\n📊 Final Scores:\n{scores}"
            )
        else:
            await update.message.reply_text(
                f"✅ {action}\n\n📊 Round {round_num} Scores:\n{scores}"
            )
    except Exception as e:
        await update.message.reply_text(f"Received update from tracker.")

# ---------- Fallback text handler ----------
async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use /start to open the Dai Di Tracker! 🃏"
    )

# ---------- SETUP ----------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    print("Bot is running...")
    app.run_polling()
