import asyncio

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_NAME = 'chat_guard_bot__database.db'
URL = f'sqlite+aiosqlite:///{DATABASE_NAME}'

engine = create_async_engine(URL, connect_args={"check_same_thread": False})
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_db())
