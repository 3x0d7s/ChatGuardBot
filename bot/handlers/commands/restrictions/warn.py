from aiogram import types, Router
from aiogram.filters import Command

from bot import util
from bot.command_parser import parse_command
from bot.config import bot
from bot.commands.warn import warn
from bot.filters.admin_restrictions_filter import AdminRestrictionsFilter

router = Router()
router.message.filter(
    AdminRestrictionsFilter()
)


@router.message(Command('warn', prefix="/!"))
async def handle_warn(message: types.Message):
    msg = message.text
    parser = parse_command(msg)
    reason = parser['reason']

    reply = message.reply_to_message

    await warn(bot=bot, chat_id=reply.chat.id, user_id=reply.from_user.id, reason=reason)
