import asyncio
import datetime
import logging
import sys
from random import randint

import config

import aiogram
from aiogram import types


bot = aiogram.Bot(token=config.BOT_TOKEN)
dp = aiogram.Dispatcher()

new_chat_member_dict = dict()


def is_bot_in_group_chat(message: types.Message):
    return message.chat.id != message.from_user.id


def generate_math_question():
    first_number = randint(2, 10)
    second_number = randint(2, 10)

    return first_number, second_number, first_number + second_number


@dp.message()
async def answer_message(message: types.Message):
    if not is_bot_in_group_chat(message):
        return

    new_chat_member_list = message.new_chat_members
    if new_chat_member_list:
        for member in new_chat_member_list:
            first_number, second_number, user_answer = generate_math_question()

            new_chat_member_dict[member.id] = user_answer
            await message.answer(text=f"Привіт, {member.full_name}\n"
                                      f"Cкільки буде {first_number} + {second_number}?")
            return

    if message.from_user.id in new_chat_member_dict:
        try:
            user_answer = int(message.text.strip())

            if user_answer == new_chat_member_dict[message.from_user.id]:
                await message.reply("Правильна відповідь!")
            else:
                raise ValueError
        except ValueError:
            time_delta = datetime.timedelta(days=5)
            block_date = datetime.datetime.now() + time_delta

            await message.reply("Неправильна відповідь!\nКористувач буде заблокований до "
                                + block_date.strftime('%d/%m/%Y %H:%M'))
            await bot.ban_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                until_date=time_delta,
                revoke_messages=False
            )

        new_chat_member_dict.pop(message.from_user.id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
