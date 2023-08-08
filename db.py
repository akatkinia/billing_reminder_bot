import sqlite3
from config import DB_PATH

def create_bill_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY,
                Дата TEXT,
                Плательщик TEXT,
                Документ TEXT,
                "Период оплаты" TEXT,
                Сумма INT
            )
        ''')

def create_messages_log_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_messages (
                id INTEGER PRIMARY KEY,
                date TEXT,
                user_id INTEGER,
                username TEXT,
                nickname TEXT,
                message TEXT
            )
        ''')

def insert_bill_record(data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bills (Дата, Плательщик, Документ, "Период оплаты", Сумма) VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
