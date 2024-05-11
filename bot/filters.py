from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot import util


class RestrictionsFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        return message.reply_to_message is not None


class AdminRestrictionsFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        if not await util.has_admin_permissions(chat=message.chat, user=message.from_user):
            return False

        return message.reply_to_message is not None
