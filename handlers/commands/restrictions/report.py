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

    response = (f'{util.mention_user(message.from_user)} '
                'відправив скаргу на '
                f'{util.mention_user(reply.from_user)}\n\n')

    msg_text = message.text[1:]  # remove / or ! prefix
    msg_text = msg_text.lstrip('report')
    if msg_text and not msg_text.isspace():
        reason = msg_text.lstrip("\n")
        response = f"{response}**Причина**:{reason}\n"

    await message.reply(text=response)

    response += (f'Група: [{message.chat.full_name}]({util.group_link(message.chat)})\n'
                 f'[Посилання на повідомлення]({util.message_link(reply)})')

    administrator_list = await util.get_list_of_administrators(message.chat)

    for administrator in administrator_list:
        user = administrator.user
        if not user.is_bot:
            await bot.send_message(chat_id=administrator.user.id, text=response)
