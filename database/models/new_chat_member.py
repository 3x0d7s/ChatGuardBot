from datetime import datetime, timedelta
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Date, delete
from sqlalchemy.orm import relationship, Session

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
    def is_(cls, chat_id: int, user_id: int, session: Session) -> bool:
        return cls.of(
            ChatMember.ensure_entity(
                chat_id=chat_id, user_id=user_id, session=session), session=session) is not None

    @classmethod
    def of(cls, chat_member: ChatMember, session: Session):
        return session.query(cls).filter_by(chat_member_id=chat_member.id).first()

    @classmethod
    def insert(cls,
               chat_member: ChatMember,
               user_answer: int,
               question_message_id: int,
               session: Session):
        session.add(cls(chat_member_id=chat_member.id,
                        user_answer=user_answer,
                        question_message_id=question_message_id))

    @classmethod
    def delete(cls, chat_member_id: int, session: Session):
        session.query(cls).filter_by(chat_member_id=chat_member_id).delete()
        session.commit()

    @classmethod
    def pop_old_records(cls, session: Session):
        current_date = datetime.now().date()
        old_records = session.query(cls).filter(cls.restriction_date < current_date).all()
        for record in old_records:
            session.delete(record)
        session.commit()
        return old_records
