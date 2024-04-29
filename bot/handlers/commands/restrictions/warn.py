from aiogram import types, Router
from aiogram.filters import Command

import util
from bot.config import bot
from bot.commands.warn import warn


router = Router()


@router.message(Command('warn', prefix="/!"))
async def handle_warn(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await warn(bot=bot, chat_id=reply.chat.id, user_id=reply.from_user.id)
