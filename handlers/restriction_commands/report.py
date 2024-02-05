from aiogram import types, Router
from aiogram.filters import Command

import util
from config import bot

router = Router()


@router.message(Command('report', prefix="/!"))
async def report(message: types.Message):
    reply = message.reply_to_message
    if not reply:
        return

    response = (f'{util.username_or_fullname(message.from_user)} '
                'відправив скаргу на '
                f'{util.username_or_fullname(reply.from_user)}\n'
                f'Чат {message.chat.full_name}\n')

    msg_text = message.text[1:]  # remove / or ! prefix
    if not msg_text.lstrip('report').isspace():
        reason = msg_text.lstrip("report\n")
        response = f"{response}\n**Причина**: {reason}"

    await message.reply(text=response)

    administrator_list = await util.get_list_of_administators(message.chat)

    for administrator in administrator_list:
        user = administrator.user
        if not user.is_bot:
            await bot.send_message(chat_id=administrator.user.id, text=response)
