import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text

        if "instagram.com" in text:
            await update.message.reply_text(
                "لینک اینستاگرام دریافت شد، در حال پردازش..."
            )
        else:
            return


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot started...")
    app.run_polling()


if name == "__main__":
    main()
