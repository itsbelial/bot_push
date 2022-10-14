from aiogram import types, Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from FSM import fsm_machine as fsm
import sqlite3
from loader import dp, bot, db, cur, loop
from markups import start_markup as kb
from libs.vk_api.longpoll import VkLongPoll, VkEventType
import libs.vk_api
import libs.vk

chat = 5364809518

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: Message):
    await bot.send_message(message.from_user.id, "test", reply_markup=kb.startMenu)

@dp.message_handler(state=None)
async def keyboard(message: Message):
    if message.text == "Помощь":
        await bot.send_message(message.from_user.id, "Message 1")
    if message.text == "Подключить уведомления":
        await fsm.FSMConnect.userToken.set()
        await message.answer("Отправь сюда свой токен ВК. Получить его можешь на сайте https://vkhost.github.io/ \n"
                             "Инструкция:\n"
                             "Выбираешь Kate Mobile(желательно с компа).\n"
                             "Потом в адрессной строке копируешь символы от \n"
                             "acces_token= до &expires_in\n"
                             "Ну и все типа. Бот запустится. Остальные кнопки работать не будут\n"
                             "чтобы отрубить его пиши мне")
    if message.text == "Настройки":
        await bot.send_message(message.from_user.id, "Message 3")

@dp.message_handler(state=fsm.FSMConnect.userToken)
async def connect_push(message: Message, state: fsm.FSMContext):
    async with state.proxy() as data:
        data['userToken'] = message.text
    token = data['userToken']
    await state.finish()
    vk_session = libs.vk_api.VkApi(token=token)
    CLIENT = libs.vk.API(token)
    longpoll = VkLongPoll(vk_session)
    await bot.send_message(message.from_user.id, "Прием сообщений запущен. Дальнейшее взаимодействие с ботом невозможно "
                                                 "из за запущенного цикла, чтобы разорвать соединение с ВК - нажмите на"
                                                 " соответствующую кнопку в меню.")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            if message.text == "Stop":
                await message.answer("stop")
                break
            user_id = event.user_id
            text = event.text
            info_user = CLIENT.users.get(user_ids=user_id, v=5.131)[0]
            await bot.send_message(chat_id=chat, text=f'*❗ {info_user["first_name"]} {info_user["last_name"]}* ❗\n\n'
                                                                f'{text}', parse_mode='Markdown')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(keyboard, state=None)
    dp.register_message_handler(connect_push, state=fsm.FSMConnect.userToken)