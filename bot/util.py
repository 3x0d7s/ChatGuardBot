from random import randint
from typing import List, Union

from aiogram import types
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator


def mention_user(user: types.User) -> str:
    if user.username:
        return "@" + user.username
    return f"[{user.full_name}](tg://user?id={user.id})"


def group_link(chat: types.Chat) -> str:
    if chat.username:
        return f"https://t.me/{chat.username}"
    chat_id = chat.id[2:]
    return f"https://t.me/c/{chat_id}"


def message_link(message: types.Message) -> str:
    if message.chat.username:
        if message.chat.is_forum:
            return f"https://t.me/{message.chat.username}/{message.message_thread_id}/{message.message_id}"
        return f"https://t.me/{message.chat.username}/{message.message_id}"
    chat_id = str(message.chat.id)[2:]
    return f"https://t.me/c/{chat_id}/{message.message_id}"


def is_bot_in_group_chat(message: types.Message) -> bool:
    return message.chat.id != message.from_user.id


async def get_list_of_administrators(chat: types.Chat) -> List[Union[ChatMemberOwner, ChatMemberAdministrator]]:
    chat_member_list: List[Union[ChatMemberOwner, ChatMemberAdministrator]] = await chat.get_administrators()
    return chat_member_list


async def has_admin_permissions(chat: types.Chat, user: types.User) -> bool:
    admin_users_list = [admin.user for admin in await get_list_of_administrators(chat)]
    return user in admin_users_list


def generate_math_question() -> tuple:
    first_number = randint(2, 10)
    second_number = randint(2, 10)
    return first_number, second_number, first_number + second_number
