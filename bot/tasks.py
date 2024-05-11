import asyncio
import datetime
import traceback

from bot.config import bot
from bot.handlers.chat_members_actions.new_chat_member import block_member_after_timeout
from database.config import sessionmaker
from database.models.chat_member import ChatMember
from database.models.new_chat_member import NewChatMember


async def handle_new_chat_members():
    while True:
        async with sessionmaker() as session:
            old_records = await NewChatMember.pop_old_records(session)
            for old_record in old_records:
                user_entry = await ChatMember.get_by_id(old_record.chat_member_id, session=session)
                chat_member = await bot.get_chat_member(chat_id=user_entry.chat_id, user_id=user_entry.user_id)
                await block_member_after_timeout(user=chat_member.user,
                                                 chat_id=user_entry.chat_id,
                                                 duration=datetime.timedelta(days=5))
        await asyncio.sleep(60)