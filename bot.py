import asyncio
import logging
import os
from os import getenv

import requests
from aiogram.filters import Command
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.DEBUG)

URL = "http://127.0.0.1:8000/upl?m={0}"

load_dotenv()

bot = Bot(token=os.getenv('BOT_API_KEY'), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()


@dp.message(Command("a"))
async def answer(message: types.Message):
    answer_text = message.text.strip("/a ")
    resp = requests.post(
        url=URL.format(answer_text),
    )
    await message.reply(resp.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
