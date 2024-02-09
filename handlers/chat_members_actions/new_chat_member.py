import asyncio
import datetime

from aiogram import types, F, Router

import util
from config import bot, db_controller


class NewUser:
    def __init__(self, chat_id, message_id, answer):
        self.chat_id = chat_id
        self.message_id = message_id
        self.answer = answer


new_chat_member_dict = dict()

router = Router()


async def block_user_after_timeout(user: types.User, chat_id: int, duration: datetime.timedelta):
    block_date = datetime.datetime.now() + duration

    await bot.send_message(
        chat_id,
        f"{util.mention_user(user)} не дав правильної відповіді на запитання протягом 1 хвилини!\nВін буде "
        f"заблокований до {block_date.strftime('%d/%m/%Y %H:%M')}"
    )
    await bot.ban_chat_member(
        chat_id=chat_id,
        user_id=user.id,
        until_date=duration,
        revoke_messages=False
    )
    new_chat_member_dict.pop(user.id)


async def handle_timeout(user: types.User, chat_id: int):
    time_delta = datetime.timedelta(minutes=1)
    block_time = datetime.datetime.now() + time_delta

    while user.id in new_chat_member_dict and datetime.datetime.now() < block_time:
        await asyncio.sleep(1)
    if user.id not in new_chat_member_dict:
        return

    duration = datetime.timedelta(days=5)
    await block_user_after_timeout(user, chat_id, duration)


@router.message(F.new_chat_members)
async def welcome_new_members(message: types.Message):
    if not util.is_bot_in_group_chat(message):
        return

    new_chat_member_list = message.new_chat_members
    for member in new_chat_member_list:
        first_number, second_number, user_answer = util.generate_math_question()
        welcome_msg = await message.answer(text=f"Привіт, {util.mention_user(member)}\n"
                                                f"Cкільки буде {first_number} + {second_number}?\n"
                                                "На відповідь дається 1 хвилина")
        new_chat_member_dict[member.id] = NewUser(chat_id=message.chat.id,
                                                  message_id=welcome_msg.message_id,
                                                  answer=user_answer)
        await message.delete()

        # Створюємо таймер для кожного нового користувача
        await asyncio.create_task(handle_timeout(member, message.chat.id))


@router.message()
async def answer_message(message: types.Message):
    if not util.is_bot_in_group_chat(message):
        return

    if message.from_user.id in new_chat_member_dict:
        try:
            user_answer = int(message.text.strip())

            if user_answer == new_chat_member_dict[message.from_user.id].answer:
                # await message.reply("Правильна відповідь!")
                db_controller.create_warn_count_row(group_id=message.chat.id, user_id=message.from_user.id)
            else:
                raise ValueError
        except ValueError:
            await block_user_after_timeout(message.from_user, message.chat.id, datetime.timedelta(days=5))
        finally:
            user = new_chat_member_dict[message.from_user.id]
            await bot.delete_message(chat_id=user.chat_id, message_id=user.message_id)
            await message.delete()
            new_chat_member_dict.pop(message.from_user.id)
