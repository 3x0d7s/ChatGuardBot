import asyncio
import datetime

from bot.config import bot
from bot.handlers.chat_members_actions.new_chat_member import block_member_after_timeout
from database.config import sessionmaker
from database.repositories.new_chat_member_repo import NewChatMemberRepo


async def handle_new_chat_members():
    while True:
        async with sessionmaker() as session:
            old_records = await NewChatMemberRepo(session).pop_old_records()
            for old_record in old_records:
                chat_member = await bot.get_chat_member(chat_id=old_record.chat_id, user_id=old_record.user_id)
                await block_member_after_timeout(user=chat_member.user,
                                                 chat_id=old_record.chat_id,
                                                 duration=datetime.timedelta(days=5))
        await asyncio.sleep(60)
