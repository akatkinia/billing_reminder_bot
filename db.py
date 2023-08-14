import sqlite3
from config import DB_PATH

def create_bill_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY,
                Date TEXT,
                Payer TEXT,
                Document TEXT,
                "Period of payment" TEXT,
                Amount INT
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
        cursor.execute('INSERT INTO bills (Date, Payer, Document, "Period of payment", Amount) VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
