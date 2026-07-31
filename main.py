import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


TOKEN = os.getenv("BOT_TOKEN")


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()


async def download_instagram(url):
    filename = "download"

    options = {
        "outtmpl": filename + ".%(ext)s",
        "format": "best",
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    if "instagram.com" not in text:
        return

    await update.message.reply_text("⏳ در حال دانلود...")

    try:
        file_path = await download_instagram(text)

        with open(file_path, "rb") as file:
            await update.message.reply_document(
                document=file
            )

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(
            "❌ خطا در دانلود\n" + str(e)
        )


def main():
    threading.Thread(target=run_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
