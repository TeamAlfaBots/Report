import asyncio
import threading
import os
from fastapi import FastAPI
import uvicorn
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database.models import init_db
from handlers.menu import router as bot_router

load_dotenv()

app = FastAPI()

@app.get("/")
async def health(): return {"status": "online"}

async def start_bot():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(bot_router)
    await dp.start_polling(bot)

def run_web_server():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

async def main():
    init_db()
    threading.Thread(target=run_web_server, daemon=True).start()
    print("[*] DeepHat is Running...")
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
