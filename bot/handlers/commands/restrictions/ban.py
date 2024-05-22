from aiogram import types, Router
from aiogram.filters import Command

from bot.command_parser import parse_command, parse_time
from bot.config import bot
from bot.restrictions.ban import ban
from bot.filters import AdminRestrictionsFilter
from database.config import sessionmaker
from database.repositories.chat_member_repo import ChatMemberRepo

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

    await (ChatMemberRepo(sessionmaker()).mark_as_unblocked(
        chat_id=message.chat.id,
        user_id=reply.from_user.id
    ))
