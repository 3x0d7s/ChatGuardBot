from aiogram import Bot

import util


async def ban(bot: Bot, chat_id: id, user_id: int, reason=''):
    await bot.ban_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        revoke_messages=False
    )

    user = (await bot.get_chat_member(chat_id=chat_id, user_id=user_id)).user
    response = f"{util.mention_user(user)} тепер заблокований у цьому чаті назавжди!"
    await bot.send_message(chat_id=chat_id, text=response)
