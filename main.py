import asyncio
import datetime
import logging
import os
import sys
from random import randint
from typing import Union, List

from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator

from db_controller import DbController

TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

db_controller = DbController('chat_bot_db')

new_chat_member_dict = dict()


def username_or_fullname(user: types.User) -> str:
    if user.username:
        return "@" + user.username
    return user.full_name


def is_bot_in_group_chat(message: types.Message) -> bool:
    return message.chat.id != message.from_user.id


async def has_admin_permissions(chat: types.Chat, user: types.User) -> bool:
    chat_member_list: List[Union[ChatMemberOwner, ChatMemberAdministrator]] = await chat.get_administrators()
    admin_users_list = [admin.user for admin in chat_member_list]
    return user in admin_users_list


def generate_math_question() -> tuple:
    first_number = randint(2, 10)
    second_number = randint(2, 10)
    return first_number, second_number, first_number + second_number


async def handle_timeout(user: types.User, chat_id: int):
    time_delta = datetime.timedelta(minutes=1)
    block_time = datetime.datetime.now() + time_delta

    while user.id in new_chat_member_dict and datetime.datetime.now() < block_time:
        await asyncio.sleep(1)
    if user.id not in new_chat_member_dict:
        return

    await block_user_after_timeout(user, chat_id, time_delta)


async def block_user_after_timeout(user: types.User, chat_id: int, duration: datetime.timedelta):
    block_date = datetime.datetime.now() + duration

    await bot.send_message(
        chat_id,
        f"{username_or_fullname(user)} не дав правильної відповіді на запитання протягом 1 хвилини!\nВін буде "
        f"заблокований до {block_date.strftime('%d/%m/%Y %H:%M')}"
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
    if not await has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        revoke_messages=False
    )
    await message.answer(text=f"{username_or_fullname(reply.from_user)} тепер забанений у цьому чаті назавжди")


@dp.message(F.text == "!unban")
@dp.message(F.text == "/unban")
async def unmute(message: types.Message):
    if not await has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id
    )


@dp.message(F.text == "!mute")
@dp.message(F.text == "/mute")
async def mute(message: types.Message):
    if not await has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=False)
    )
    await message.answer(
        text=f"{username_or_fullname(reply.from_user)} тепер обмежений у правах надсилати повідомлення!")


@dp.message(F.text == "!unmute")
@dp.message(F.text == "/unmute")
async def unmute(message: types.Message):
    if not await has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=reply.from_user.id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=True)
    )


@dp.message(F.text == "!warn")
@dp.message(F.text == "/warn")
async def warn(message: types.Message):
    if not await has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    warned_count = db_controller.warn_user(group_id=message.chat.id, user_id=reply.from_user.id)
    if warned_count >= 3:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            revoke_messages=False
        )
        await message.answer(text=f"{username_or_fullname(reply.from_user)} тепер забанений у цьому чаті назавжди")
    else:
        await message.reply(text=f"{username_or_fullname(reply.from_user)} має ({warned_count}/3) попереджень! ")


@dp.message(F.text == "/help")
async def send_help(message: types.Message):
    help_text = ("**Cписок команд**:\n"
                 "/ban - забанити користувача\n"
                 "/mute - обмежити користувача у правах надсилання повідомлень\n"
                 "/unban - забанити користувача\n"
                 "/unmute - зняти обмеження у користувача у правах надсилання повідомлень\n"
                 "Команду треба прописати, відповідаючи(reply) на повідомлення користувача, до якого ви "
                 "хочете застосувати відповідну дію\n"
                 "Також можна прописувати вищезгадані команди зі знаком ! замість / у початку.\n")

    await message.answer(help_text)


@dp.message(F.new_chat_members)
async def greeting_new_members(message: types.Message):
    if not is_bot_in_group_chat(message):
        return

    new_chat_member_list = message.new_chat_members
    for member in new_chat_member_list:
        first_number, second_number, user_answer = generate_math_question()
        new_chat_member_dict[member.id] = (user_answer,
                                           datetime.datetime.now() + datetime.timedelta(minutes=1))
        await message.answer(text=f"Привіт, {username_or_fullname(member)}\n"
                                  f"Cкільки буде {first_number} + {second_number}?\n"
                                  "На відповідь дається 1 хвилина")
        # Створюємо таймер для кожного нового користувача
        await asyncio.create_task(handle_timeout(member, message.chat.id))


@dp.message()
async def answer_message(message: types.Message):
    if not is_bot_in_group_chat(message):
        return

    if message.from_user.id in new_chat_member_dict:
        try:
            user_answer = int(message.text.strip())

            if user_answer == new_chat_member_dict[message.from_user.id][0]:
                await message.reply("Правильна відповідь!")
                db_controller.create_warn_count_row(group_id=message.chat.id, user_id=message.from_user.id)
                new_chat_member_dict.pop(message.from_user.id)
            else:
                raise ValueError
        except ValueError:
            await block_user_after_timeout(message.from_user, message.chat.id, datetime.timedelta(days=5))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
