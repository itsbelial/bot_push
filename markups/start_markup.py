from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

btnHelp = KeyboardButton("Помощь")
btnPush = KeyboardButton("Подключить уведомления")
btnSettings = KeyboardButton("Настройки")

startMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnHelp, btnSettings).row(btnPush)