from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command('help'))
async def send_help(message: types.Message):
    help_text = ("**Cписок команд для адмінстраторів**:\n"
                 "/ban - заблокувати користувача у цій групі.\n"
                 "/mute - обмежити користувача у правах надсилання повідомлень.\n"
                 "/unban - зняти блокування користувача у цій групі.\n"
                 "/unmute - зняти обмеження у користувача у правах надсилання повідомлень.\n"
                 "/warn - попередження(якщо користувач отримує 3 попередження, його заблокуюють).\n\n"

                 "вищезгадані команди також можна прописувати зі знаком ! замість / у початку!.\n\n"

                 "**Список команд для користувачів**:\n"
                 "/report - кинути скаргу на користувача за надіслане ним повідомлення.\n"

                 "Команду треба прописати, відповідаючи(reply) на повідомлення користувача, до якого ви "
                 "хочете застосувати відповідну дію\n")

    await message.answer(help_text)