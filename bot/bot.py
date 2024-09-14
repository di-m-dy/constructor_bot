"""
Main file to run the bot
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import router

from config import TG_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TG_TOKEN)

dp = Dispatcher()
dp.include_router(router)


async def start():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
