from aiogram import Bot, types

from bot import util


async def mute(bot: Bot, chat_id: id, user_id: int, reason=''):
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=False)
    )

    user = (await bot.get_chat_member(chat_id=chat_id, user_id=user_id)).user
    response = f"{util.mention_user(user)} тепер обмежений у правах надсилати повідомлення!"
    if reason:
        response += f"\nПричина: {reason}"

    await bot.send_message(chat_id=chat_id, text=response)
