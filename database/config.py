import asyncio

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_NAME = 'chat_guard_bot__database.db'

engine = create_async_engine(f'sqlite+aiosqlite:///{DATABASE_NAME}', connect_args={"check_same_thread": False})
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


# def create_db():
#     Base.metadata.create_all(engine)
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_db())
