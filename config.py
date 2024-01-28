import os

from aiogram import Bot
from aiogram.enums import ParseMode

from db_controller import DbController

TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
db_controller = DbController('chat_bot_db')