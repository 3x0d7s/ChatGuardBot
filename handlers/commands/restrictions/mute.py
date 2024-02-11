from aiogram import types, Router
from aiogram.filters import Command

import util
from config import bot

router = Router()


@router.message(Command('mute', prefix='/!'))
async def mute(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=False)
    )

    response = f"{util.mention_user(reply.from_user)} тепер обмежений у правах надсилати повідомлення!"

    msg_text = message.text[1:]  # remove / or ! prefix
    msg_text = msg_text.lstrip('mute')
    if msg_text and not msg_text.isspace():
        reason = msg_text.lstrip("\n")
        response = f"{response}\n**Причина**:{reason}"

    await message.answer(text=response)


@router.message(Command('unmute', prefix='/!'))
async def unmute(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=True)
    )
