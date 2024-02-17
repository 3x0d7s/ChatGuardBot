import asyncio
import datetime

from aiogram import types, F, Router

import util
from bot import bot, db_controller


class NewUser:
    def __init__(self, chat_id, message_id, answer):
        self.chat_id = chat_id
        self.message_id = message_id
        self.answer = answer


# new_chat_member_dict = dict()

# async def start_block_member_task():
#     await asyncio.create_task(handle_new_chat_members())

router = Router()


async def block_member_after_timeout(user: types.User, chat_id: int, duration: datetime.timedelta):
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
    # new_chat_member_dict[chat_id].pop(user.id)
    # db_controller.delete_non_responded_new_members()


# async def handle_timeout(user: types.User, chat_id: int):
#     time_delta = datetime.timedelta(minutes=1)
#     block_time = datetime.datetime.now() + time_delta
#
#     # while user.id in new_chat_member_dict[chat_id] and datetime.datetime.now() < block_time:
#     #     await asyncio.sleep(1)
#     # if user.id not in new_chat_member_dict[chat_id]:
#     #     return
#
#     duration = datetime.timedelta(days=5)
#     await block_user_after_timeout(user, chat_id, duration)

async def handle_new_chat_members():
    while True:
        # await asyncio.sleep(60)
        non_responded_new_member_list = db_controller.pop_non_responded_new_member_entities()
        for new_member in non_responded_new_member_list:
            chat_id = new_member[1]
            user = bot.get_chat_member(chat_id=chat_id, user_id=new_member[0])
            await block_member_after_timeout(user=user, chat_id=chat_id)


@router.message(F.new_chat_members)
async def welcome_new_members(message: types.Message):
    if not util.is_bot_in_group_chat(message):
        return

    new_chat_member_list = message.new_chat_members
    for member in new_chat_member_list:
        first_number, second_number, user_answer = util.generate_math_question()
        welcome_message = await message.answer(text=f"Привіт, {util.mention_user(member)}\n"
                                                f"Cкільки буде {first_number} + {second_number}?\n"
                                                "На відповідь дається 1 хвилина")
        db_controller.create_new_member_row(chat_id=message.chat.id,
                                            user_id=member.id,
                                            answer=user_answer,
                                            question_message_id = welcome_message.message_id,
                                            restriction_date=datetime.datetime.now() + datetime.timedelta(minutes=1))
        await message.delete()

        # Створюємо таймер для кожного нового користувача
        # await asyncio.create_task(handle_timeout(member, message.chat.id))
        # await asyncio.create_task(handle_new_chat_members())


@router.message(F.func(
    lambda msg: msg.from_user.id == db_controller.if_exists(chat_id=msg.chat.id, user_id=msg.from_user.id)))
async def answer_message(message: types.Message):
    if not util.is_bot_in_group_chat(message):
        return

    user = message.from_user
    question_message_id = db_controller.get_question_message_id(chat_id=message.chat.id, user_id=user.id)
    try:
        user_answer = int(message.text.strip())
        if user_answer == db_controller.get_answer(user_id=user.id, chat_id=message.chat.id):
            # await message.reply("Правильна відповідь!")
            db_controller.create_warn_count_row(chat_id=message.chat.id, user_id=user.id)
        else:
            raise ValueError
    except ValueError:
        await block_member_after_timeout(user, message.chat.id, datetime.timedelta(days=5))
    finally:
        await bot.delete_message(chat_id=message.chat.id, message_id=question_message_id)
        await message.delete()
        db_controller.delete_new_member(chat_id=message.chat.id, user_id=user.id)


# asyncio.create_task(handle_new_chat_members())
