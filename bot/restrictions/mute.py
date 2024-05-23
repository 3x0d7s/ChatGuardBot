from datetime import datetime

from aiogram import Bot, types

from bot import util


async def mute(bot: Bot,
               chat_id: id,
               user_id: int,
               reason: str = '',
               until_date: datetime = None):
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=False),
        until_date=until_date
    )

    user = (await bot.get_chat_member(chat_id=chat_id, user_id=user_id)).user
    response = f"{user.mention_markdown()} тепер обмежений у правах надсилати повідомлення!"

    if reason:
        response += f"\nПричина: {reason}"
    if until_date:
        response += f"\nОбмеження триває до {until_date.strftime('%d.%m.%Y')}"

    await bot.send_message(chat_id=chat_id, text=response)
