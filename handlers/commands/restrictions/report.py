from enum import Enum

from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, User

import util
from bot import bot
from database.config import Sessions
from database.models.chat_member import ChatMember
from database.models.warns import Warns

router = Router()


class Action(str, Enum):
    ban = "ban"
    mute = "mute"
    warn = "warn"


class AdminAction(CallbackData, prefix="adm"):
    action: Action
    chat_id: int
    user_id: int
    reason: str


def report_btn_markup(chat_id: int, user_id: int, reason: str) -> InlineKeyboardMarkup:
    warn_btn = InlineKeyboardButton(
        text="Warn",
        callback_data=AdminAction(action="warn", chat_id=chat_id, user_id=user_id, reason=reason).pack()
    )
    mute_btn = InlineKeyboardButton(
        text="Mute",
        callback_data=AdminAction(action="mute", chat_id=chat_id, user_id=user_id, reason=reason).pack()
    )
    ban_btn = InlineKeyboardButton(
        text="Ban",
        callback_data=AdminAction(action="ban", chat_id=chat_id, user_id=user_id, reason=reason).pack()
    )

    rows = [[warn_btn], [mute_btn, ban_btn]]
    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.message(Command('report', prefix="/!"))
async def report(message: types.Message):
    reply = message.reply_to_message
    if not reply:
        return

    response = (f'{util.mention_user(message.from_user)} '
                'відправив скаргу на '
                f'{util.mention_user(reply.from_user)}\n\n')

    msg_text = message.text[1:]  # remove / or ! prefix
    msg_text = msg_text.lstrip('report')
    reason = ''

    if msg_text and not msg_text.isspace():
        reason = msg_text.lstrip("\n")
        response = f"{response}**Причина**:{reason}\n"

    await message.reply(text=response)

    response += (f'Група: [{message.chat.full_name}]({util.group_link(message.chat)})\n'
                 f'[Посилання на повідомлення]({util.message_link(reply)})')

    administrator_list = await util.get_list_of_administrators(message.chat)

    for administrator in administrator_list:
        user = administrator.user
        if not user.is_bot:
            await bot.send_message(chat_id=administrator.user.id,
                                   text=response,
                                   reply_markup=report_btn_markup(chat_id=reply.chat.id,
                                                                  user_id=reply.from_user.id,
                                                                  reason=reason))


@router.callback_query(AdminAction.filter(F.action == Action.ban))
async def ban_user(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    await bot.ban_chat_member(
        chat_id=callback_data.chat_id,
        user_id=callback_data.user_id,
        revoke_messages=False
    )

    chat_member = await bot.get_chat_member(chat_id=callback_data.chat_id, user_id=callback_data.user_id)

    response = f"{util.mention_user(chat_member.user)} тепер заблокований у цьому чаті назавжди!"
    response = f"{response}\n**Причина**: {callback_data.reason}"

    await bot.send_message(chat_id=callback_data.chat_id, text=response)


@router.callback_query(AdminAction.filter(F.action == Action.mute))
async def mute_user(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    await bot.restrict_chat_member(
        chat_id=callback_data.chat_id,
        user_id=callback_data.user_id,
        permissions=types.chat_permissions.ChatPermissions(can_send_messages=False)
    )

    chat_member_user = await bot.get_chat_member(chat_id=callback_data.chat_id, user_id=callback_data.user_id)

    response = f"{util.mention_user(chat_member_user.user)} тепер обмежений у правах надсилати повідомлення!"
    response = f"{response}\n**Причина**: {callback_data.reason}"

    await bot.send_message(chat_id=callback_data.chat_id, text=response)


@router.callback_query(AdminAction.filter(F.action == Action.warn))
async def warn_user(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    with Sessions() as session:
        chat_member = ChatMember.ensure_entity(chat_id=callback_data.chat_id,
                                               user_id=callback_data.user_id,
                                               session=session)
        warned_count = Warns.increase(chat_member=chat_member, session=session)

        chat_member_user = await bot.get_chat_member(chat_id=callback_data.chat_id, user_id=callback_data.user_id)

        response = f"{util.mention_user(chat_member_user.user)} має {warned_count}/3 попереджень! "

        await bot.send_message(chat_id=callback_data.chat_id, text=response)

        if warned_count >= 3:
            await bot.ban_chat_member(
                chat_id=callback_data.chat_id,
                user_id=callback_data.user_id,
                revoke_messages=False
            )
            await bot.send_message(chat_id=callback_data.chat_id,
                                   text=f"{util.mention_user(chat_member_user.user)} тепер заблокований у цьому чаті назавжди!")
            Warns.delete(chat_member=chat_member, session=session)
