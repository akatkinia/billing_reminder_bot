from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp
from create_bot import ProfileStatesGroup
from datetime import datetime
from db import insert_bill_record


# Обработка команд 'start' и cancel
# @dp.message_handler(commands=['start', 'cancel'], state='*')
async def cmd_start_cancel(message: types.Message, state: FSMContext):
    await ProfileStatesGroup.Document.set()
    await message.answer(text=f"""Добро пожаловать, {message.from_user.full_name}!
Введите документ (например, '<code>ЕПД</code>'):""", parse_mode='html')
    
# Обработчик данных "Документ"
# @dp.message_handler(state=ProfileStatesGroup.Document)
async def get_period(message: types.Message, state: FSMContext):
    # Сохраняем данные "Документ" в состояние
    # await state.update_data(Doc=message.text)
    async with state.proxy() as data:
        data['Doc'] = message.text
    # Назначаем состоянием "Период оплаты"
    await ProfileStatesGroup.Period.set()
    await message.answer("Введите период оплаты (например, '<code>01.2023</code>'):", parse_mode='html')

# Обработчик данных "Период оплаты"
# @dp.message_handler(state=ProfileStatesGroup.Period)
async def get_amount(message: types.Message, state: FSMContext):
    # Сохраняем данные "Период оплаты" в состояние
    # await state.update_data(Per=message.text)
    async with state.proxy() as data:
        data['Per'] = message.text
    await ProfileStatesGroup.Amount.set()
    await message.answer('Введите сумму оплаты:')

# Обработчик данных "Сумма" и сохранение информации в БД
# @dp.message_handler(state=ProfileStatesGroup.Amount)
async def save_to_database(message: types.Message, state: FSMContext):
    # Сохраняем данные "Сумма" в состояние
    # await state.update_data(Amm=message.text)
    async with state.proxy() as data:
        data['Amm'] = message.text

    # Получаем текущую дату
    current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    username = message.from_user.full_name

    # Сохраняем данные из состояния в БД
    async with state.proxy() as data:
        db_data = (
            current_date,
            username,
            data['Doc'],
            data['Per'],
            data['Amm']
        )
        insert_bill_record(db_data)

    # Сбрасываем состояние после завершения обработки
    await state.finish()
    await message.answer('Спасибо! Ты лучше всех!')


########### Регистрация обработчиков ##########################################################
# Команды для регистрации handlers для бота - они передаются в основной файл bot.py
def register_handlers_common(dp: dp):
    dp.register_message_handler(cmd_start_cancel, commands=['start', 'cancel'], state='*')
    dp.register_message_handler(get_period, state=ProfileStatesGroup.Document)
    dp.register_message_handler(get_amount, state=ProfileStatesGroup.Period)
    dp.register_message_handler(save_to_database, state=ProfileStatesGroup.Amount)
