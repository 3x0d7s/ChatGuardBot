import datetime

from aiogram import types, F, Router

from bot import util
from bot.config import bot
from database.config import sessionmaker
from database.repositories.chat_member_repo import ChatMemberRepo
from database.repositories.new_chat_member_repo import NewChatMemberRepo

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

    await (ChatMemberRepo(sessionmaker()).mark_as_blocked(
        chat_id=chat_id,
        user_id=user.id
    ))


async def introduce_itself(chat_id: int):
    await bot.send_message(chat_id=chat_id,
                           text="Привіт! Дякую що добавили мене у цей чат.\n"
                                "Для того щоб користуватися командами - надайте мені права, зокрема на блокування "
                                "користувачів.\n"
                                "Для отримання опису для чого призначений цей бот введіть команду - /description\n"
                                "Перелік доступних команд та їх опис - /help")


async def welcome_new_user(message: types.Message, user: types.User):
    first_number, second_number, user_answer = util.generate_math_question()
    welcome_message = await message.answer(text=f"Привіт, {util.mention_user(user)}\n"
                                                f"Cкільки буде {first_number} + {second_number}?\n"
                                                "На відповідь дається 1 хвилина")
    async with sessionmaker() as session:
        await NewChatMemberRepo(session=session).insert(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            user_answer=user_answer,
            question_message_id=welcome_message.message_id
        )


@router.message(F.new_chat_members)
async def new_members(message: types.Message):
    new_chat_member_list = message.new_chat_members
    for user in new_chat_member_list:
        if user.is_bot:
            if user.id == bot.id:
                await introduce_itself(message.chat.id)
        else:
            await welcome_new_user(message, user)
        await message.delete()


@router.message(F.func(lambda msg: NewChatMemberRepo(sessionmaker())
                       .check_if_exists(chat_id=msg.chat.id,
                                        user_id=msg.from_user.id)))
async def answer_message(message: types.Message):
    if not util.is_bot_in_group_chat(message):
        return

    async with sessionmaker() as session:
        user = message.from_user

        new_chat_member_repo = NewChatMemberRepo(session=session)
        new_chat_member = await new_chat_member_repo.get(
            chat_id=message.chat.id,
            user_id=message.from_user.id)
        question_message_id = new_chat_member.question_message_id

        try:
            user_answer = int(message.text.strip())
            if user_answer == new_chat_member.user_answer:
                # await message.reply("Правильна відповідь!")
                await ChatMemberRepo(session=session).insert_if_absent(
                    chat_id=new_chat_member.chat_id,
                    user_id=new_chat_member.user_id)
            else:
                raise ValueError
        except ValueError:
            await block_member_after_timeout(user, message.chat.id, datetime.timedelta(days=5))
        finally:
            await bot.delete_message(chat_id=message.chat.id, message_id=question_message_id)
            await message.delete()
            await new_chat_member_repo.delete(
                chat_id=message.chat.id,
                user_id=message.from_user.id
            )
