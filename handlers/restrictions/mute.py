from aiogram import F, types, Router
from aiogram.filters import Command

import util
from config import bot

router = Router()


@router.message(F.text == "!mute")
@router.message(Command('mute'))
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
    await message.answer(
        text=f"{util.username_or_fullname(reply.from_user)} тепер обмежений у правах надсилати повідомлення!")


@router.message(F.text == "!unmute")
@router.message(Command('unmute'))
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
