from aiogram import Bot

import util
from database.config import sessionmaker
from database.models.chat_member import ChatMember
from database.models.warns import Warns


async def warn(bot: Bot, chat_id: id, user_id: int, reason=''):
    async with sessionmaker() as session:
        chat_member_user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

        chat_member = await ChatMember.ensure_entity(chat_id=chat_id,
                                                     user_id=user_id,
                                                     session=session)
        warned_count = await Warns.increase(chat_member=chat_member, session=session)

        response = f"{util.mention_user(chat_member_user.user)} має {warned_count}/3 попереджень! "

        await bot.send_message(chat_id=chat_id, text=response)

        if warned_count >= 3:
            await bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                revoke_messages=False
            )
            user = (await bot.get_chat_member(chat_id=chat_id, user_id=user_id)).user

            msg = f"{util.mention_user(user)} тепер заблокований у цьому чаті назавжди!"
            await bot.send_message(chat_id=chat_id, text=msg)
            await Warns.delete(chat_member=chat_member, session=session)
