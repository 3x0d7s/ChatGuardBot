from typing import Type, TypeVar, Generic

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepo(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, chat_id: int, user_id: int):
        select_smth = (
            select(self.model).filter_by(
                chat_id=chat_id,
                user_id=user_id
            )
        )

        result = await self.session.execute(select_smth)

        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, chat_id: int, user_id: int):
        query = select(self.model).filter_by(chat_id=chat_id, user_id=user_id)
        result = (await self.session.execute(query)).scalar()
        if result:
            await self.session.delete(result)
            await self.session.commit()
