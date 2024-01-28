from random import randint
from typing import List, Union

from aiogram import types
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator


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