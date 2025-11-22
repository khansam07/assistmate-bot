import os
import asyncio
import httpx
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

async def start(update, context):
    await update.message.reply_text("🤖 AssistMate AI Bot\n\nHello! Powered by Llama 3.1! Kuch bhi pucho!")

async def handle_message(update, context):
    try:
        user_message = update.message.text
        await update.message.chat.send_action(action="typing")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [{"role": "user", "content": user_message}]
                },
                timeout=30.0
            )
            
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            await update.message.reply_text(ai_response)
            
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
        print(f"Error: {e}")

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot running with OpenRouter!")
    print("🚀 Powered by Llama 3.1")
    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("⛔ Bot stopped!")

if __name__ == '__main__':
    asyncio.run(run_bot())
