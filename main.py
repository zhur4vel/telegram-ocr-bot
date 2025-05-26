import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OCR_API_KEY = os.getenv("OCR_API_KEY")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()

        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": photo_bytes},
            data={"apikey": OCR_API_KEY, "language": "pol"}
        )

        result = response.json()

        if result.get("IsErroredOnProcessing"):
            error_message = result.get("ErrorMessage", ["Неизвестная ошибка"])[0]
            await update.message.reply_text("❌ OCR API вернула ошибку: " + error_message)
            return

        parsed_results = result.get("ParsedResults")
        if not parsed_results:
            await update.message.reply_text("⚠️ Не удалось извлечь текст.")
            return

        text = parsed_results[0].get("ParsedText", "")
        await update.message.reply_text("📄 Распознанный текст:\n\n" + text)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
