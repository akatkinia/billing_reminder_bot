import logging
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.handler import CancelHandler
from datetime import datetime
import sqlite3

from config import ADMIN_ID, ALLOW_IDS, DB_PATH, TOKEN_API, WEBHOOK_URL
from db import create_bill_table, create_messages_log_table


storage = MemoryStorage()

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(filename='./persistant_data/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', encoding='utf-8')
dp.middleware.setup(LoggingMiddleware())


class ProfileStatesGroup(StatesGroup):
    Document = State()
    Period = State()
    Amount = State()

class LoggingMiddleware(BaseMiddleware):
    # middleware для захвата сообщений пользователя перед другими обработчиками message_handler - запись в БД и лог-файл
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Проверка ID пользователя для доступа к боту
        if message.from_user.id not in ALLOW_IDS:
            print(f'{message.from_user.full_name} - {message.from_user.id}')
            await message.answer(text=f"{message.from_user.full_name} не имеет доступа")
            raise CancelHandler()
        else:
            user_id = message.from_user.id
            nickname = message.from_user.username
            username = message.from_user.full_name
            text = message.text
            current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
            # Запись сообщений от пользователей в БД users_messages
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users_messages (date, user_id, username, nickname, message) VALUES (?, ?, ?, ?, ?)',
                            (current_date_time, user_id, username, nickname, text if text else None))
                conn.commit()
            except Exception as ex:
                logging.error(f"Exception: {ex}")    
            finally:
                cursor.close()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        # middleware для захвата callback queries от пользователя - запись в лог-файл
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username
        data = callback_query.data
        logging.info(f"Received callback query from user {user_id} (@{username}): {data}")    

async def on_startup(dp):
    logging.warning('Starting up...')
    await bot.set_webhook(WEBHOOK_URL)
    # создание таблиц
    create_messages_log_table()
    create_bill_table()
    # создание постоянного соединения с БД при запуске бота
    global conn
    conn = sqlite3.connect(DB_PATH)
    await bot.send_message(chat_id=ADMIN_ID, text=f'Billing bot is online')

async def on_shutdown(dp):
    logging.warning('Shutting down...')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    session = await bot.get_session()
    await session.close()
    # закрытия соединения с БД при завершении работы бота
    conn.close()
    await bot.send_message(chat_id=ADMIN_ID, text=f'Billing bot is offline')
    logging.warning('Bye!')
