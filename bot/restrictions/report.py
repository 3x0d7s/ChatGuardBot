from aiogram import Bot
from aiogram.types import Message

from bot import util
from bot.btn_markup import report_btn_markup


async def report(bot: Bot,
                 chat_id: id,
                 user_id: int,
                 message: Message,
                 response: str = '',
                 reason: str = ''):
    if reason:
        response += f"Причина: {reason}\n"

    await bot.send_message(chat_id=chat_id, text=response)

    chat = await bot.get_chat(chat_id=chat_id)

    response += (f'Група: [{chat.full_name}]({util.group_link(chat)})\n'
                 f'[Посилання на повідомлення]({util.message_link(message)})')

    administrator_list = await util.get_list_of_administrators(chat)

    for administrator in administrator_list:
        user = administrator.user
        if not user.is_bot:
            await bot.send_message(chat_id=administrator.user.id,
                                   text=response,
                                   reply_markup=report_btn_markup(chat_id=chat_id,
                                                                  user_id=user_id,
                                                                  reason=reason))
