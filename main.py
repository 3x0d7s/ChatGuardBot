import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from bot import config
from bot.handlers.chat_members_actions import left_chat_member, new_chat_member
from bot.handlers.commands.about import description, help
from bot.handlers.commands.restrictions import ban, warn, mute, report
from bot.handlers import callback_queries

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
                       left_chat_member.router,
                       new_chat_member.router,
                       callback_queries.router)
    await set_commands(config.bot)
    await dp.start_polling(config.bot)
    await new_chat_member.handle_new_chat_members()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
