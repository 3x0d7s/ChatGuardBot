import asyncio
import logging
import sys

from aiogram import Dispatcher, F, Bot
from aiogram import types
from aiogram.filters import Command
from aiogram.types import BotCommand

from config import bot
from handlers import new_chat_member_check
from handlers.restrictions import ban, mute, warn, report
from handlers.about import help, description

dp = Dispatcher()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='help',
            description="Cписок доступних команд"
        ),
        BotCommand(
            command='description',
            description="Короткий опис того, для чого потрібний цей бот."
        ),
        BotCommand(
            command='ban',
            description="Заблокувати користувача у цій групі."
        ),
        BotCommand(
            command='mute',
            description="Обмежити користувача у правах надсилання повідомлень."
        ),
        BotCommand(
            command='unban',
            description="Зняти блокування користувача у цій групі."
        ),
        BotCommand(
            command='unmute',
            description="Зняти обмеження у користувача у правах надсилання повідомлень."
        ),
        BotCommand(
            command='warn',
            description="Попередження(якщо користувач отримує 3 попередження, його заблокуюють)."
        ),
        BotCommand(
            command='report',
            description="Кинути скаргу на користувача за надіслане ним повідомлення."
        )
    ]
    await bot.set_my_commands(commands=commands)


async def main():
    dp.include_routers(warn.router,
                       ban.router,
                       mute.router,
                       report.router,
                       help.router,
                       description.router,
                       new_chat_member_check.router,)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
