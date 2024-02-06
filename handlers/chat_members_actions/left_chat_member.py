from aiogram import types, F, Router

router = Router()


@router.message(F.left_chat_members)
async def left_member_handle(message: types.Message):
    await message.delete()
