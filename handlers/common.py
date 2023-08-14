<<<<<<< HEAD
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
=======
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from config import DB_PATH
from create_bot import dp, ProfileStatesGroup
from db import insert_bill_record
from modules.save_to_file import save_csv, save_txt, save_xlsx


# ОБРАБОТЧИКИ
# Обработка команды start - запрос данных о типе документа
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await ProfileStatesGroup.Document.set()
    await message.answer(text=f"""Привет, {message.from_user.full_name}!
Введите документ (например, '<code>ЕПД</code>'):""", parse_mode="html")

# Обработка команды cancel
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Произведена отмена записи. Как будешь готов внести данные, нажми /start")

# Обработка команды help
async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer(text="""Бот помогает отслеживать данные по счетам за коммунальные услуги 🏡

<b>Список комманд:</b>
/start — начать работу с ботом. После успешного внесения показателей происходит автоматическое создание записи в базе данных
/cancel — отмена записи и сброс состояний бота
/save_xlsx — получить данные из БД в формате xlsx
/save_csv — получить данные из БД в формате csv
/save_txt — получить данные из БД в формате txt                                               
""",
parse_mode="html")


# Обработчик данных "Документ" + установка состояния "Период"
async def get_period(message: types.Message, state: FSMContext):
    # Сохраняем данные "Документ" в состояние
    async with state.proxy() as data:
        data['Doc'] = message.text
    # Назначаем состояние "Период оплаты"
    await ProfileStatesGroup.Period.set()
    await message.answer("Введите период оплаты (например, '<code>01.2023</code>'):", parse_mode='html')

# Обработчик данных "Период оплаты" + установка состояния "Сумма"
async def get_amount(message: types.Message, state: FSMContext):
    # Сохраняем данные "Период оплаты" в состояние
    async with state.proxy() as data:
        data['Per'] = message.text
    await ProfileStatesGroup.Amount.set()
    await message.answer("Введите сумму оплаты:")

# Обработчик данных "Сумма" и сохранение информации в БД
async def save_to_database(message: types.Message, state: FSMContext):
    # Сохраняем данные "Сумма" в состояние
>>>>>>> main
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
<<<<<<< HEAD
    await message.answer('Спасибо! Ты лучше всех!')


########### Регистрация обработчиков ##########################################################
# Команды для регистрации handlers для бота - они передаются в основной файл bot.py
def register_handlers_common(dp: dp):
    dp.register_message_handler(cmd_start_cancel, commands=['start', 'cancel'], state='*')
    dp.register_message_handler(get_period, state=ProfileStatesGroup.Document)
    dp.register_message_handler(get_amount, state=ProfileStatesGroup.Period)
    dp.register_message_handler(save_to_database, state=ProfileStatesGroup.Amount)
=======
    await message.answer("Спасибо! Увидимся в следующем месяце!")


# ЭКСПОРТ ИЗ БД
# Экспорт в csv
async def send_csv(message: types.Message):
    save_csv(DB_PATH)
    with open('./persistant_data/database.csv', 'rb') as csv_file:
        await message.answer_document(document=InputFile(csv_file))

# Экспорт в xlsx
async def send_xlsx(message: types.Message):
    save_xlsx(DB_PATH)
    with open('./persistant_data/database.xlsx', 'rb') as xlsx_file:
        await message.answer_document(document=InputFile(xlsx_file))

# Экспорт в txt
async def send_txt(message: types.Message):
    save_txt(DB_PATH)
    with open('./persistant_data/database.txt', 'rb') as txt_file:
        await message.answer_document(document=InputFile(txt_file))


# РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ
def register_handlers_common(dp: dp):
    dp.register_message_handler(send_csv, commands=['save_csv'], state='*')
    dp.register_message_handler(send_xlsx, commands=['save_xlsx'], state='*')
    dp.register_message_handler(send_txt, commands=['save_txt'], state='*')

    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_help, commands=['help'], state='*')

    dp.register_message_handler(get_period, state=ProfileStatesGroup.Document)
    dp.register_message_handler(get_amount, state=ProfileStatesGroup.Period)
    dp.register_message_handler(save_to_database, state=ProfileStatesGroup.Amount)

>>>>>>> main
