from aiogram import F, types, Router

from config import db_controller, bot
import util

router = Router()


@router.message(F.text == "!warn")
@router.message(F.text == "/warn")
async def warn(message: types.Message):
    if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
        return

    reply = message.reply_to_message
    if not reply:
        return

    warned_count = db_controller.warn_user(group_id=message.chat.id, user_id=reply.from_user.id)
    if warned_count >= 3:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            revoke_messages=False
        )
        await message.answer(text=f"{util.username_or_fullname(reply.from_user)} тепер забанений у цьому чаті назавжди")
        db_controller.delete_warn_count(group_id=message.chat.id, user_id=reply.from_user.id)
    else:
        await message.reply(text=f"{util.username_or_fullname(reply.from_user)} має ({warned_count}/3) попереджень! ")