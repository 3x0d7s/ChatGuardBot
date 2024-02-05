from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command('description'))
async def send_description(message: types.Message):
    help_text = ("Бот - сторож групи. "
                 "Опитує приєднаних до групи нових користувачів просте питання-капчу, на які вони повинні відповісти "
                 "протягом однієї хвилини."
                 "Інакше він їх блокує як спам-ботів на 5 днів.\n"
                 "Також надає команди обмежень над користувачами групи. Список та їх тлумачення яких можна глянути "
                 "ввіши команду \help."
                 )

    await message.answer(help_text)