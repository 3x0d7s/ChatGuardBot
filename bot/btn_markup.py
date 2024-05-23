from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks import AdminAction


def report_btn_markup(chat_id: int, user_id: int, reason: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Warn",
                callback_data=AdminAction(action="warn", chat_id=chat_id, user_id=user_id, reason=reason).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Mute",
                callback_data=AdminAction(action="mute", chat_id=chat_id, user_id=user_id, reason=reason).pack()
            ),
            InlineKeyboardButton(
                text="Ban",
                callback_data=AdminAction(action="ban", chat_id=chat_id, user_id=user_id, reason=reason).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
