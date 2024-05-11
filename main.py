import asyncio
import logging
import sys

from aiogram import Dispatcher

from bot import config
from bot.commands import set_commands
from bot.handlers.chat_members_actions import left_chat_member, new_chat_member
from bot.handlers.commands.about import description, help
from bot.handlers.commands.restrictions import ban, warn, mute, report
from bot.handlers import callback_queries
from bot.tasks import handle_new_chat_members
from database.config import create_db

dp = Dispatcher()


async def start_bot():
    handle_new_chat_members_task = asyncio.create_task(handle_new_chat_members())

    # await create_db()

    dp.include_routers(warn.router,
                       ban.router,
                       mute.router,
                       report.router,
                       help.router,
                       description.router,
                       left_chat_member.router,
                       new_chat_member.router,
                       callback_queries.router)
    await config.bot.delete_webhook(drop_pending_updates=True)
    await set_commands(config.bot)
    await dp.start_polling(config.bot)

    await handle_new_chat_members_task


async def main():
    await start_bot()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
