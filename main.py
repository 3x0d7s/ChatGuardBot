import asyncio
import logging
import sys

from aiogram import Dispatcher, F
from aiogram import types

from config import bot
from handlers import new_chat_member_check
from handlers.restrictions import ban, mute, warn, report

dp = Dispatcher()


@dp.message(F.text == "/help")
async def send_help(message: types.Message):
    help_text = ("**Cписок команд**:\n"
                 "/ban - забанити користувача\n"
                 "/mute - обмежити користувача у правах надсилання повідомлень\n"
                 "/unban - забанити користувача\n"
                 "/unmute - зняти обмеження у користувача у правах надсилання повідомлень\n"
                 "/warn - попередження\n"
                 "Команду треба прописати, відповідаючи(reply) на повідомлення користувача, до якого ви "
                 "хочете застосувати відповідну дію\n"
                 "Також можна прописувати вищезгадані команди зі знаком ! замість / у початку.\n")

    await message.answer(help_text)


async def main():
    dp.include_routers(warn.router, ban.router, mute.router, report.router, new_chat_member_check.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
