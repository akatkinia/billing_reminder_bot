import logging
# import os

from datetime import datetime
from aiogram import Dispatcher, Bot, types
from config import TOKEN_API
from config import WEBHOOK_URL
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import ADMIN_ID
from aiogram.dispatcher.handler import CancelHandler

import sqlite3
from config import DB_PATH
from db import create_bill_table, create_messages_log_table

storage = MemoryStorage()

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot, storage=storage)

# Класс с состояниями для FSM
class ProfileStatesGroup(StatesGroup):
    Document = State()
    Period = State()
    Amount = State()

ALLOW_IDS = [] # сюда необходимо добавить список тех USER_ID которые будут иметь доступ к боту

# добавляем middleware on_pre_process_message перед другими обработчиками message_handler для захвата сообщений пользователя
class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # ЗАПИСЬ СООБЩЕНИЙ ОТ ПОЛЬЗОВАТЕЛЕЙ В БД users_messages
        # Проверка ID пользователя для доступа к боту
        if message.from_user.id not in ALLOW_IDS:
            print(f'{message.from_user.full_name} - {message.from_user.id}')
            await message.answer(text=f"{message.from_user.full_name} не имеет доступа")
            raise CancelHandler()
        else:
            # print(f'{message.from_user.full_name} - {message.from_user.id}')
            user_id = message.from_user.id
            nickname = message.from_user.username
            username = message.from_user.full_name
            text = message.text
            current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users_messages (date, user_id, username, nickname, message) VALUES (?, ?, ?, ?, ?)',
                            (current_date_time, user_id, username, nickname, text if text else None))
                conn.commit()
            except Exception as ex:
                # В случае ошибки откатить изменения
                # conn.rollback()
                logging.error(f"!!!ERROR!!!: {ex}")    
                print("Ошибка:", ex)
            finally:
                cursor.close()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        # ЛОГИРОВАНИЕ CALLBACK QUERY ОТ ПОЛЬЗОВАТЕЛЕЙ
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username
        data = callback_query.data
        logging.info(f"Received callback query from user {user_id} (@{username}): {data}")    

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', encoding='utf-8')
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    logging.warning('Starting up...')
    # insert code here to run it after start
    await bot.set_webhook(WEBHOOK_URL)
    # создание таблиц
    create_messages_log_table()
    create_bill_table()
    global conn
    conn = sqlite3.connect(DB_PATH)
    await bot.send_message(chat_id=ADMIN_ID, text=f'Billing bot is online')


async def on_shutdown(dp):
    logging.warning('Shutting down...')
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await bot.get_session()
    await session.close()
    conn.close()
    await bot.send_message(chat_id=ADMIN_ID, text=f'Billing bot is offline')

    logging.warning('Bye!')
