import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import templates

TELEGRAM_BOT_TOKEN = getenv("RF_PDD_TESTS_BOT_API")

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
   await message.answer(templates.USER_BOT_START)


@router.message(Command("help"))
async def echo_handler(message: types.Message) -> None:
    try:
        await message.answer(templates.USER_BOT_HELP)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
