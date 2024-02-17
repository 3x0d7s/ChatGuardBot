from aiogram import types, F, Router

from bot import db_controller

router = Router()


@router.message(F.left_chat_member)
async def left_member_handle(message: types.Message):
    db_controller.delete_warn_count_row(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.delete()
