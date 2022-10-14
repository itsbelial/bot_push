from aiogram.utils import executor
from loader import bot, dp
from handlers import client

client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True)