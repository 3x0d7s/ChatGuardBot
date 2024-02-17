from aiogram import types, Router
from aiogram.filters import Command

import util
from bot import db_controller, bot

router = Router()


@router.message(Command('warn', prefix="/!"))
async def warn(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    warned_count = db_controller.warn_user(chat_id=message.chat.id, user_id=reply.from_user.id)

    response = f"{util.mention_user(reply.from_user)} має ({warned_count}/3) попереджень! "

    msg_text = message.text[1:]  # remove / or ! prefix
    msg_text = msg_text.lstrip('warn')
    if msg_text and not msg_text.isspace():
        reason = msg_text.lstrip("\n")
        response = f"{response}\n**Причина**:{reason}"

    await message.reply(text=response)

    if warned_count >= 3:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            revoke_messages=False
        )
        await message.answer(text=f"{util.mention_user(reply.from_user)} тепер заблокований у цьому чаті назавжди!")
        db_controller.delete_warn_count_row(chat_id=message.chat.id, user_id=reply.from_user.id)