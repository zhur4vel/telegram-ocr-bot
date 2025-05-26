import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OCR_API_KEY = os.getenv("OCR_API_KEY")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"filename": photo_bytes},
        data={"apikey": OCR_API_KEY, "language": "pol"},
    )

    result = response.json()
    text = result["ParsedResults"][0]["ParsedText"]
    await update.message.reply_text(f"📄 Распознанный текст:\n\n{text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()  # ← ЭТО ГЛАВНОЕ
