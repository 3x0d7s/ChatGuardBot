import asyncio
import datetime

from aiogram import types, F, Router

import util
from bot import bot

from database.config import Sessions
from database.models.chat_member import ChatMember
from database.models.new_chat_member import NewChatMember
from database.models.warns import Warns

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


async def handle_new_chat_members():
    while True:
        await asyncio.sleep(60)
        with Sessions() as session:
            old_records = NewChatMember.pop_old_records(session)
            for old_record in old_records:
                user_entry = ChatMember.get_by_id(old_record.chat_member_id, session=session)
                user = bot.get_chat_member(chat_id=user_entry.chat_id, user_id=user_entry.user_id)
                await block_member_after_timeout(user=user,
                                                 chat_id=user_entry.chat_id,
                                                 duration=datetime.timedelta(days=5))


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
        with Sessions() as session:
            member_info = ChatMember.ensure_entity(chat_id=message.chat.id,
                                                   user_id=message.from_user.id,
                                                   session=session)
            session.commit()
            NewChatMember.insert(chat_member=member_info,
                                 user_answer=user_answer,
                                 question_message_id=welcome_message.message_id,
                                 session=session)
            session.commit()
        await message.delete()


@router.message(F.func(lambda msg: NewChatMember.is_(chat_id=msg.chat.id,
                                                     user_id=msg.from_user.id,
                                                     session=Sessions())))
async def answer_message(message: types.Message):
    if not util.is_bot_in_group_chat(message):
        return

    with Sessions() as session:
        user = message.from_user

        chat_member = ChatMember.ensure_entity(chat_id=message.chat.id, user_id=message.from_user.id, session=session)
        new_chat_member = NewChatMember.of(chat_member=chat_member, session=session)

        question_message_id = new_chat_member.question_message_id

        try:
            user_answer = int(message.text.strip())
            if user_answer == new_chat_member.user_answer:
                # await message.reply("Правильна відповідь!")
                Warns.create(chat_member_id=chat_member.id, session=session)
            else:
                raise ValueError
        except ValueError:
            await block_member_after_timeout(user, message.chat.id, datetime.timedelta(days=5))
        finally:
            await bot.delete_message(chat_id=message.chat.id, message_id=question_message_id)
            await message.delete()
            NewChatMember.delete(chat_member_id=chat_member.id, session=session)
