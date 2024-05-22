from sqlalchemy import update, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.chat_member import ChatMember
from database.repositories.base_repo import BaseRepo


class ChatMemberRepo(BaseRepo[ChatMember]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChatMember)

    async def insert(self,
                     chat_id: int,
                     user_id: int) -> ChatMember:
        insert_stmt = (
            insert(ChatMember)
            .values(
                chat_id=chat_id,
                user_id=user_id,
                warn_count=0
            )
            .returning(ChatMember)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def with_increased_warn_count(self, chat_id: int, user_id: int):
        # update_stmt = (
        #     update(ChatMember)
        #     .filter_by(
        #         chat_id=chat_id,
        #         user_id=user_id,
        #     )
        #     .values({'warn_count': ChatMember.warn_count + 1})
        #     .returning(ChatMember)
        # )

        select_stmt = select(ChatMember).filter_by(chat_id=chat_id, user_id=user_id)
        result = await self.session.execute(select_stmt)
        chat_member = result.scalar_one_or_none()

        if chat_member:
            stmt = (
                update(ChatMember)
                .filter_by(chat_id=chat_id, user_id=user_id)
                .values(warn_count=ChatMember.warn_count + 1)
                .returning(ChatMember)
            )
        else:
            stmt = (
                insert(ChatMember)
                .values(chat_id=chat_id, user_id=user_id, warn_count=1)
                .returning(ChatMember)
            )
        result = await self.session.execute(stmt)

        await self.session.commit()
        return result.scalar_one()

    async def mark_as_blocked(self, chat_id: int, user_id: int):
        update_stmt = (
            update(ChatMember)
            .filter_by(
                chat_id=chat_id,
                user_id=user_id,
            )
            .values({'is_blocked': True})
            .returning(ChatMember)
        )
        await self.session.execute(update_stmt)
        await self.session.commit()

    async def mark_as_unblocked(self, chat_id: int, user_id: int):
        update_stmt = (
            update(ChatMember)
            .filter_by(
                chat_id=chat_id,
                user_id=user_id,
            )
            .values({'is_blocked': False,
                     'warn_count': 0})
            .returning(ChatMember)
        )
        await self.session.execute(update_stmt)
        await self.session.commit()
