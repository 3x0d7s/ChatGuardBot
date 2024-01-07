import asyncio
import datetime
import logging
import sys
from random import randint

import config

from aiogram import Bot, Dispatcher, F
from aiogram import types

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

new_chat_member_dict = dict()


def username_or_fullname(user: types.User):
    if user.username:
        return "@" + user.username
    return user.full_name


def is_bot_in_group_chat(message: types.Message):
    return message.chat.id != message.from_user.id


def generate_math_question():
    first_number = randint(2, 10)
    second_number = randint(2, 10)
    return first_number, second_number, first_number + second_number


async def handle_timeout(user: types.User, chat_id: int):
    time_delta = datetime.timedelta(minutes=1)
    block_date = datetime.datetime.now() + time_delta

    while user.id in new_chat_member_dict and datetime.datetime.now() < block_date:
        await asyncio.sleep(1)
    if user.id not in new_chat_member_dict:
        return

    await block_user(user, chat_id, time_delta)


async def block_user(user: types.User, chat_id: int, duration: datetime.timedelta):
    block_date = datetime.datetime.now() + duration

    await bot.send_message(
        chat_id,
        f"{username_or_fullname(user)} не дав правильної відповіді на запитання протягом 1 хвилини!\nВін буде заблокований до {block_date.strftime('%d/%m/%Y %H:%M')}"
    )
    await bot.ban_chat_member(
        chat_id=chat_id,
        user_id=user.id,
        until_date=duration,
        revoke_messages=False
    )
    new_chat_member_dict.pop(user.id)


@dp.message(F.text == "!ban")
@dp.message(F.text == "/ban")
async def ban(message: types.Message):
    reply = message.reply_to_message
    if not reply:
        return

    await bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        revoke_messages=False
    )
    await message.answer(text=f"{username_or_fullname(reply.from_user)} був забанений у цьому чаті назавжди")


@dp.message()
async def answer_message(message: types.Message):
    if not is_bot_in_group_chat(message):
        return

    new_chat_member_list = message.new_chat_members
    if new_chat_member_list:
        for member in new_chat_member_list:
            first_number, second_number, user_answer = generate_math_question()

            new_chat_member_dict[member.id] = (user_answer,
                                               datetime.datetime.now() + datetime.timedelta(minutes=1))
            await message.answer(text=f"Привіт, {username_or_fullname(member)}\n"
                                      f"Cкільки буде {first_number} + {second_number}?\n"
                                      "На відповідь дається 1 хвилина")

            # Створюємо таймер для кожного нового користувача
            await asyncio.create_task(handle_timeout(member, message.chat.id))

            return

    if message.from_user.id in new_chat_member_dict:
        try:
            user_answer = int(message.text.strip())

            if user_answer == new_chat_member_dict[message.from_user.id][0]:
                await message.reply("Правильна відповідь!")
                new_chat_member_dict.pop(message.from_user.id)
            else:
                raise ValueError
        except ValueError:
            await block_user(message.from_user, message.chat.id, datetime.timedelta(days=5))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
