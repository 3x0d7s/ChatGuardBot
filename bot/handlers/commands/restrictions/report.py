from aiogram import types, Router
from aiogram.filters import Command

from bot import util
from bot.command_parser import parse_command
from bot.restrictions.report import report
from bot.config import bot
from bot.filters import RestrictionsFilter

router = Router()
router.message.filter(
    RestrictionsFilter()
)


@router.message(Command('report', prefix="/!"))
async def handle_report(message: types.Message):
    reply = message.reply_to_message

    response = (f'{message.from_user.mention_markdown()} '
                'відправив скаргу на '
                f'{reply.from_user.mention_markdown()}\n\n')

    msg = message.text
    parser = parse_command(msg)
    reason = parser['reason']

    await report(bot=bot,
                 chat_id=message.chat.id,
                 user_id=reply.from_user.id,
                 message=reply,
                 response=response,
                 reason=reason)
