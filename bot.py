import os
import asyncio
import google.generativeai as genai
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
async def start(update, context):
    await update.message.reply_text("🤖 AssistMate AI Bot\n\nHello! Kuch bhi pucho!")

async def handle_message(update, context):
    try:
        user_message = update.message.text
        await update.message.chat.send_action(action="typing")
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot running!")
    
    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ Bot stopped!")

if __name__ == '__main__':
    asyncio.run(run_bot())
