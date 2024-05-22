from sqlalchemy import Integer, Boolean, false
from sqlalchemy.orm import mapped_column, Mapped

from database.config import Base


class ChatMember(Base):
    __tablename__ = 'chat_member'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    warn_count: Mapped[int] = mapped_column(Integer)
    is_blocked: Mapped[bool] = mapped_column(Boolean, server_default=false())
