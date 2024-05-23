from aiogram import Bot

from bot import util
from database.config import sessionmaker
from database.repositories.chat_member_repo import ChatMemberRepo


async def warn(bot: Bot,
               chat_id: id,
               user_id: int,
               reason: str = ''):
    async with sessionmaker() as session:
        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

        chat_member_repo = ChatMemberRepo(session)
        chat_member_entry = await chat_member_repo.get(chat_id=chat_id, user_id=user_id)
        if chat_member_entry and chat_member_entry.is_blocked:
            return
        chat_member_entry = await chat_member_repo.with_increased_warn_count(chat_id=chat_id, user_id=user_id)

        warned_count = chat_member_entry.warn_count

        response = f"{chat_member.user.mention_markdown()} має {warned_count}/3 попереджень! "
        if reason:
            response += f"\nПричина останнього попередження: {reason}"

        await bot.send_message(chat_id=chat_id, text=response)

        if warned_count >= 3:
            await bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                revoke_messages=False
            )
            user = (await bot.get_chat_member(chat_id=chat_id, user_id=user_id)).user

            await chat_member_repo.mark_as_blocked(chat_id=chat_id, user_id=user_id)
            msg = f"{user.mention_markdown()} тепер заблокований у цьому чаті назавжди!"
            await bot.send_message(chat_id=chat_id, text=msg)
