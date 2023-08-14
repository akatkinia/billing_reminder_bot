#!/usr/bin/env python3

from datetime import datetime
import requests

from config import ALLOW_IDS
from config import TOKEN_API


def send_message(user_id):
    r = requests.post(url=URL, data={
    "chat_id": {user_id},
    "text": "👋\nГотов ли внести данные по счетам ЖКУ?\nНажми /start"
})


def month_check():
    if MONTH %2 == 0:
        send_message(ALLOW_IDS[0])
    else:
        send_message(ALLOW_IDS[1])

def main():
    month_check()


if __name__ == '__main__':
    URL=f"https://api.telegram.org/bot{TOKEN_API}/sendMessage"
    MONTH = datetime.now().month
    
    main()
