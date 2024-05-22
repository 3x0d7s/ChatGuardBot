from datetime import datetime, timedelta

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.sqlite import insert

from database.models.new_chat_member import NewChatMember
from database.repositories.base_repo import BaseRepo


class NewChatMemberRepo(BaseRepo[NewChatMember]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NewChatMember)

    async def insert(self,
                     chat_id: int,
                     user_id: int,
                     user_answer: int,
                     question_message_id: int) -> NewChatMember:
        insert_stmt = (
            insert(NewChatMember)
            .values(
                chat_id=chat_id,
                user_id=user_id,
                user_answer=user_answer,
                question_message_id=question_message_id,
                restriction_datetime=datetime.now() + timedelta(minutes=1)
            )
            .returning(NewChatMember)
        )

        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def get(self, chat_id: int, user_id: int):
        select_smth = (
            select(NewChatMember).filter_by(
                chat_id=chat_id,
                user_id=user_id
            )
        )

        result = await self.session.execute(select_smth)

        await self.session.commit()
        return result.scalar_one()

    async def check_if_exists(self, chat_id: int, user_id: int) -> bool:
        return self.get(chat_id=chat_id,
                        user_id=user_id) is not None
