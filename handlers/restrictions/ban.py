from aiogram import F, types, Router
from aiogram.filters import Command

from config import bot
import util

router = Router()


@router.message(F.text == "!ban")
@router.message(Command('ban'))
async def ban(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        revoke_messages=False
    )
    await message.answer(text=f"{util.username_or_fullname(reply.from_user)} тепер забанений у цьому чаті назавжди")


@router.message(F.text == "!unban")
@router.message(Command('unban'))
async def unban(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id
    )
