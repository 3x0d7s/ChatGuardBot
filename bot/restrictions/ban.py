from datetime import datetime

from aiogram import Bot

from bot import util


async def ban(bot: Bot,
              chat_id: id,
              user_id: int,
              reason: str = '',
              until_date: datetime = None):
    await bot.ban_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        revoke_messages=False,
        until_date=until_date
    )

    user = (await bot.get_chat_member(chat_id=chat_id, user_id=user_id)).user
    response = f"{user.mention_markdown()} тепер заблокований у цьому чаті назавжди!"

    if reason:
        response += f"\nПричина блокування: {reason}"
    if until_date:
        response += f"\nОбмеження триває до {until_date.strftime('%d.%m.%Y')}"

    await bot.send_message(chat_id=chat_id, text=response)
