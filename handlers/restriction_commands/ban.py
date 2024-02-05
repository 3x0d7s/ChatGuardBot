from aiogram import types, Router
from aiogram.filters import Command

import util
from config import bot

router = Router()


@router.message(Command('ban', prefix='/!'))
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

    msg_text = message.text[1:]  # remove / or ! prefix
    response = f"{util.username_or_fullname(reply.from_user)} тепер заблокований у цьому чаті назавжди!"
    if not msg_text.lstrip('ban').isspace():
        reason = msg_text.lstrip("ban\n")
        response = f"{response}\n**Причина**: {reason}"

    await message.answer(text=response)


@router.message(Command('unban', prefix='/!'))
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
