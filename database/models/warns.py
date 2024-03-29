from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Session

from database.models.chat_member import ChatMember
from database.config import Base


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
    def of(cls, chat_member: ChatMember, session: Session):
        return session.query(cls).filter_by(chat_member_id=chat_member.id).one()

    @classmethod
    def create(cls, chat_member_id: int, session: Session):
        if not session.query(cls).filter_by(chat_member_id=chat_member_id).one_or_none():
            session.add(cls(chat_member_id=chat_member_id, warn_count=0))
        session.commit()

    @classmethod
    def increase(cls, chat_member: ChatMember, session: Session):
        return (session.query(cls)
                  .filter_by(chat_member_id=chat_member.id)
                  .update({'warn_count': cls.warn_count + 1}))

    @classmethod
    def delete(cls, chat_member: ChatMember, session: Session):
        session.query(cls).filter(chat_member_id=chat_member.id).delete()
        session.commit()
