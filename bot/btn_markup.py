from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks import AdminAction


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