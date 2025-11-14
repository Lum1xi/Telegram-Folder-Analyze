from datetime import datetime

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from aiogram.types import Message

from bots.handlers.setup import setup_router
from bots.handlers.start import start_router
from config import BOT_TOKEN as TOKEN
from database import init_db
from bots.telethon_service import client

async def main():
    storage = MemoryStorage()
    async with Bot(token=TOKEN) as bot:
        await bot.delete_webhook(drop_pending_updates=True)

        dp = Dispatcher(bot=bot, storage=storage)

        dp.include_router(setup_router)
        dp.include_router(start_router)
        await init_db()
        await client.start()
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
