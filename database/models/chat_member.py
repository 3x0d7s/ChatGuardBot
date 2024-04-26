from sqlalchemy import Column, Integer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from database.config import Base


class ChatMember(Base):
    __tablename__ = 'chat_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    user_id = Column(Integer)

    warns = relationship('Warns', back_populates='chat_member')
    new_chat_member = relationship('NewChatMember', back_populates='chat_member')

    def __init__(self, chat_id, user_id):
        self.chat_id = chat_id
        self.user_id = user_id

    @classmethod
    async def ensure_entity(cls, chat_id: int, user_id: int, session: AsyncSession):
        async with session:
            query = select(cls).filter_by(chat_id=chat_id, user_id=user_id)
            result = (await session.execute(query)).scalar()
            if not result:
                result = cls(chat_id=chat_id, user_id=user_id)
                session.add(result)
                await session.commit()
            return result

    @classmethod
    async def get_by_id(cls, id: int, session: AsyncSession):
        async with session:
            query = select().filter_by(id=id)
            return (await session.execute(query)).scalar()
