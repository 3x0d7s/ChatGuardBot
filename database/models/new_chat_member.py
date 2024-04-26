from datetime import datetime, timedelta
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Date, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Session
from sqlalchemy import select, delete

from database.models.chat_member import ChatMember
from database.config import Base


class NewChatMember(Base):
    __tablename__ = 'new_chat_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_member_id = Column(Integer, ForeignKey('chat_member.id'))
    user_answer = Column(Integer)
    question_message_id = Column(Integer)
    restriction_date = Column(Date)

    chat_member = relationship('ChatMember', back_populates='new_chat_member')

    def __init__(self, chat_member_id: int, user_answer: int, question_message_id: int):
        self.chat_member_id = chat_member_id
        self.user_answer = user_answer
        self.question_message_id = question_message_id
        self.restriction_date = datetime.now() + timedelta(minutes=1)

    @classmethod
    async def is_(cls, chat_id: int, user_id: int, session: AsyncSession) -> bool:
        return await cls.of(
            await ChatMember.ensure_entity(
                chat_id=chat_id, user_id=user_id, session=session), session=session) is not None

    @classmethod
    async def of(cls, chat_member: ChatMember, session: AsyncSession):
        # return session.query(cls).filter_by(chat_member_id=chat_member.id).first()
        async with session:
            query = select(cls).filter_by(chat_member_id=chat_member.id)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def insert(cls,
                     chat_member: ChatMember,
                     user_answer: int,
                     question_message_id: int,
                     session: AsyncSession):
        async with session:
            session.add(cls(chat_member_id=chat_member.id,
                            user_answer=user_answer,
                            question_message_id=question_message_id))
            await session.commit()

    @classmethod
    async def delete(cls, chat_member_id: int, session: AsyncSession):
        async with session:
            query = select(cls).filter_by(chat_member_id=chat_member_id)
            selected = (await session.execute(query)).scalar()
            await session.delete(selected)
            await session.commit()

    @classmethod
    async def pop_old_records(cls, session: AsyncSession):
        async with session:
            current_date = datetime.now().date()

            query = select(cls).where(cls.restriction_date < current_date)
            entities = (await session.execute(query)).scalars()
            for entity in entities:
                await session.delete(entity)
            await session.commit()
            return entities
