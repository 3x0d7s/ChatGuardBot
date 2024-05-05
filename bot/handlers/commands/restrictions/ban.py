from aiogram import types, Router
from aiogram.filters import Command

from bot import util
from bot.command_parser import parse_command, parse_time
from bot.config import bot
from bot.commands.ban import ban
from bot.filters.admin_restrictions_filter import AdminRestrictionsFilter

router = Router()
router.message.filter(
    AdminRestrictionsFilter()
)


@router.message(Command('ban', prefix='/!'))
async def handle_ban(message: types.Message):
    parser = parse_command(message.text)
    reason = parser['reason']
    until_date = parse_time(parser['duration'])

    reply = message.reply_to_message

    await ban(bot=bot,
              chat_id=reply.chat.id,
              user_id=reply.from_user.id,
              reason=reason,
              until_date=until_date)


@router.message(Command('unban', prefix='/!'))
async def handle_unban(message: types.Message):
    reply = message.reply_to_message

    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id
    )
