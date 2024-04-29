from aiogram import types, F, Router


router = Router()


@router.message(F.left_chat_member)
async def left_member_handle(message: types.Message):
    await message.delete()
