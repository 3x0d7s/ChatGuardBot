from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, Session

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
    def ensure_entity(cls, chat_id: int, user_id: int, session: Session):
        entity = session.query(cls).filter_by(chat_id=chat_id, user_id=user_id).first()
        if not entity:
            entity = cls(chat_id=chat_id, user_id=user_id)
            session.add(entity)
        return entity

