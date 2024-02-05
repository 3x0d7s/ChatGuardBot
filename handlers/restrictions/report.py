from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.types import TextQuote

import util
from config import bot

router = Router()


@router.message(F.text == "!report")
@router.message(Command('report'))
async def report(message: types.Message):
    reply = message.reply_to_message
    if not reply:
        return

    report_info = (f'{util.username_or_fullname(message.from_user)} '
                   'відправив скаргу на '
                   f'{util.username_or_fullname(reply.from_user)}')
    report_details = (f'Чат {message.chat.full_name}\n'
                      f'Текст повідомлення, на яке було надіслано скаргу: \n')

    quote = TextQuote(text=reply.text, is_manual=True, position=len(report_info) + len(report_details))

    await message.reply(text=report_info)

    administrator_list = await util.get_list_of_administators(message.chat)

    for administrator in administrator_list:
        user = administrator.user
        if not user.is_bot:
            await bot.send_message(chat_id=administrator.user.id, text=report_info + '\n' + report_details, quote=quote)
