from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_NAME = 'chat_guard_bot__database.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Sessions = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)