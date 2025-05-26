import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8028223146:AABH5sdpdqlZxvPa8h9k9zgR3IDpuLb7jY"
OCR_API_KEY = os.getenv("OCR_API_KEY")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={'filename': photo_bytes},
        data={'apikey': OCR_API_KEY, 'language': 'pol'}
    )

    result = response.json()
    text = result['ParsedResults'][0]['ParsedText']
    await update.message.reply_text("📄 Распознанный текст:\n\n" + text)

async def main():
    print("🚀 Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    await app.initialize()
    await app.start()
    print("✅ Bot is running...")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
