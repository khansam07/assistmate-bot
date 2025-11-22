import os
import asyncio
from groq import Groq
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

from groq import Client
client = Client(api_key=GROQ_API_KEY)

async def start(update, context):
    await update.message.reply_text("🤖 AssistMate AI Bot\n\nHello! Powered by Llama 3.3! Kuch bhi pucho!")

async def handle_message(update, context):
    try:
        user_message = update.message.text
        await update.message.chat.send_action(action="typing")
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama-3.3-70b-versatile",
        )
        
        response_text = chat_completion.choices[0].message.content
        await update.message.reply_text(response_text)
            
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
        print(f"Error: {e}")

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot running with Groq AI!")
    print("🚀 Powered by Llama 3.3 70B")
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

