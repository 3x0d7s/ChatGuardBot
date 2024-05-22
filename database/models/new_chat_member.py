from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database.config import Base


class NewChatMember(Base):
    __tablename__ = 'new_chat_member'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    user_answer: Mapped[int] = mapped_column(Integer)
    question_message_id: Mapped[int] = mapped_column(Integer)
    restriction_datetime: Mapped[datetime] = mapped_column(DateTime)
