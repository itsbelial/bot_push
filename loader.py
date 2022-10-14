import asyncio
from aiogram import Bot, Dispatcher
from config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

db = sqlite3.connect("db/database.db")
cur = db.cursor()
storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=storage)