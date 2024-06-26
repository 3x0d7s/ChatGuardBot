from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot.callbacks import AdminAction, Action
from bot.restrictions.ban import ban
from bot.restrictions.mute import mute
from bot.restrictions.warn import warn

router = Router()


@router.callback_query(AdminAction.filter(F.action == Action.ban))
async def ban_user(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    await ban(bot=bot,
              chat_id=callback_data.chat_id,
              user_id=callback_data.user_id,
              reason=callback_data.reason)
    await query.answer(text="ban", show_alert=False)


@router.callback_query(AdminAction.filter(F.action == Action.mute))
async def mute_user(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    await mute(bot=bot,
               chat_id=callback_data.chat_id,
               user_id=callback_data.user_id,
               reason=callback_data.reason)
    await query.answer(text="mute", show_alert=False)


@router.callback_query(AdminAction.filter(F.action == Action.warn))
async def warn_user(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    await warn(bot=bot,
               chat_id=callback_data.chat_id,
               user_id=callback_data.user_id,
               reason=callback_data.reason)
    await query.answer(text=f"test {callback_data.user_id}", show_alert=False)
