import os

from aiogram import Bot
from aiogram.enums import ParseMode

TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)