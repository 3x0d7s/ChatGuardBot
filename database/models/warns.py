from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.chat_member import ChatMember
from database.config import Base

from sqlalchemy import select, update


class Warns(Base):
    __tablename__ = 'warns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_member_id = Column(Integer, ForeignKey('chat_member.id'))
    warn_count = Column(Integer)

    chat_member = relationship('ChatMember', back_populates='warns')

    def __init__(self, chat_member_id, warn_count):
        self.chat_member_id = chat_member_id
        self.warn_count = warn_count

    @classmethod
    async def ensure_entity(cls, chat_member: ChatMember, session: AsyncSession):
        async with session:
            query = select(cls).filter_by(chat_member_id=chat_member.id)
            result = (await session.execute(query)).scalar()
            if not result:
                result = cls(chat_member.id, 1)
                session.add(result)
                await session.commit()
            return result

    @classmethod
    async def create(cls, chat_member_id: int, session: AsyncSession):
        async with session:
            query = select(cls).filter_by(chat_member_id=chat_member_id)
            result = (await session.execute(query)).one_or_none()
            if not result:
                session.add(cls(chat_member_id=chat_member_id, warn_count=0))
            await session.commit()

    @classmethod
    async def increase(cls, chat_member: ChatMember, session: AsyncSession):
        async with session:
            # query = select(cls).filter_by(chat_member_id=chat_member.id)
            # result = await session.execute(query)
            # result = result.scalar_one()

            result = await cls.ensure_entity(chat_member, session)
            stmt = (
                update(cls)
                .filter_by(chat_member_id=chat_member.id)
                .values({'warn_count': cls.warn_count + 1})
            )
            await session.execute(stmt)
            await session.commit()

            return result.warn_count

    @classmethod
    async def delete(cls, chat_member: ChatMember, session: AsyncSession):
        async with session:
            query = select(cls).filter_by(chat_member_id=chat_member.id)
            result = (await session.execute(query)).scalar()
            await session.delete(result)
            await session.commit()
