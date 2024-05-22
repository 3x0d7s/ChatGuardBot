from aiogram import types, F, Router

from database.config import sessionmaker
from database.repositories.chat_member_repo import ChatMemberRepo

router = Router()


@router.message(F.left_chat_member)
async def left_member_handle(message: types.Message):
    await message.delete()