from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='help',
            description="Cписок доступних команд"
        ),
        BotCommand(
            command='description',
            description="Короткий опис того, для чого потрібний цей бот."
        ),
        BotCommand(
            command='ban',
            description="Заблокувати користувача у цій групі."
        ),
        BotCommand(
            command='mute',
            description="Обмежити користувача у правах надсилання повідомлень."
        ),
        BotCommand(
            command='unban',
            description="Зняти блокування користувача у цій групі."
        ),
        BotCommand(
            command='unmute',
            description="Зняти обмеження у користувача у правах надсилання повідомлень."
        ),
        BotCommand(
            command='warn',
            description="Попередження(якщо користувач отримує 3 попередження, його заблокуюють)."
        ),
        BotCommand(
            command='report',
            description="Кинути скаргу на користувача за надіслане ним повідомлення."
        )
    ]
    await bot.set_my_commands(commands=commands)