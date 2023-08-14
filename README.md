<<<<<<< HEAD
# billing_notify
Бот написан на aiogram.  
Имеет возможность ограничить доступ только для определённого списка пользователей.  
Принимает команды /start и /cancel  
При обращении задаёт уточняющие вопросы для записи в SQLite БД bills.db по столбцам:
=======
# ENG

## About Bot 
The bot is designed to remind specific users on a monthly basis to make utility payments. By querying the user, the bot records payment history data in a sqlite3 database. The payment history can be queried by the user and will be exported from the database in one of the following formats:  
* csv
* xlsx
* txt
  
  
**Database structure bills.db table bills:**
* id
* Date
* Payer
* Document
* Period of payment
* Amount
  
  
Logging of user actions to a separate table users_messages is implemented.  
**Bills.db database structure of users_messages table:**
* id
* date
* user_id
* username
* nickname
* message

The bot has a system of access and private notifications - access to the bot have only those users that are defined in the ALLOW_IDS list, which is set in the configuration file.
By default, all actions are logged in the /persistant_data/app.log file

## How to use
By default, notifications occur on the 11th of each month at 17:00 (GMT+3), but this can be overridden in the cron.config file.  
The configuration in the config.py file must be done before running:
* <code>TOKEN_API</code> - Your Telegram API token
* <code>ADMIN_ID</code> - Your id. Necessary to notify the administrator about bot operation, such as start/end (used in create_bot.py)
* <code>ALLOW_IDS</code> - List of user ids (used in notify.py and create_bot.py)
* <code>DOMAIN_NAME</code> - Domain name of the server on which the bot is running
* <code>WEBHOOK_SSL_CERT</code> - Path to your SSL certificate (default ./persistant_data/certs/fullchain.pem)
* <code>WEBHOOK_SSL_PRIV</code> - Path to the private key of your SSL certificate (default ./persistant_data/certs/privkey.pem)

### Commands:  
<code>/start</code> - Starting the recording process  
<code>/cancel</code> - Canceling an entry  
<code>/help</code> - Help output about working with the bot  
<code>/save_xlsx</code> - Export database data of bills table in xlsx format  
<code>/save_csv</code> - Export database data of bills table in csv format  
<code>/save_txt</code> - Export database data of bills table in txt format  

## Project assembly
Building a docker image  
<code>docker build -t billing_bot .</code>

## Launch
Launching from a catalog with a project:  
<code>docker run -d -p 443:443 -v /root/projects/billing_bot/containered/persistant_data:/app/persistant_data --restart=always --name billing billing_bot</code>


____

# RUS

## О боте 
Бот создан для ежемесячного напоминания конкретным пользователям о необходимости выполнения платежей за коммунальные услуги. Опрашивая пользователя, бот записывает данные об истории платежей в sqlite3 БД. История платежей может быть запрошена пользователем и будет экспортирована из БД в одном из следующих форматах:  
* csv
* xlsx
* txt
  
  
**Структура БД bills.db таблицы bills:**
>>>>>>> main
* id
* Дата
* Плательщик
* Документ
* Период оплаты
* Сумма
<<<<<<< HEAD

В будущих обновлениях появится:
* Возможность экспорта таблицы из БД в форматированный файл xlsx по запросу.
* Обращения к списку пользователей раз в месяц с вопросом о готовности внести данные. Пользователю задаются дополнительным флагом при вызове отдельного скрипта, который добавляется в cron.
* Упаковка проекта в Docker-контейнер.
=======
  
  
Реализованно логирование действий пользователя в отдельную таблицу users_messages.  
**Структура БД bills.db таблицы users_messages:**
* id
* date
* user_id
* username
* nickname
* message

У бота реализована система доступов и приватных оповещнений - доступ к боту имеют только те пользователи, что опредлены в списке ALLOW_IDS, который задаётся в файле конфигурации.
По умолчанию все действия логируются в файле /persistant_data/app.log

## Как пользоваться
По умолчанию нотификация происходят 11-го числа каждого месяца в 17:00 (GMT+3), но это может быть переопределно в крон-файле cron.config.  
Перед запуском необходимо выполнить конфигурацию в файле config.py:
* <code>TOKEN_API</code> - Ваш Telegram API токен
* <code>ADMIN_ID</code> - Ваш id. Необходим для оповещения администратора о работе бота, таких как старт/завершение работы (используется в create_bot.py)
* <code>ALLOW_IDS</code> - Список id пользователей (используется в notify.py и create_bot.py)
* <code>DOMAIN_NAME</code> - Доменное имя сервера, на котором запускается бот
* <code>WEBHOOK_SSL_CERT</code> - Путь до вашего SSL-сертификата (по умолчанию ./persistant_data/certs/fullchain.pem)
* <code>WEBHOOK_SSL_PRIV</code> - Путь до приватного ключа вашего SSL-сертификата (по умолчанию ./persistant_data/certs/privkey.pem)

### Команды:  
<code>/start</code> - Запуск процесса записи  
<code>/cancel</code> - Отмена записи  
<code>/help</code> - Вывод справки о работе с ботом  
<code>/save_xlsx</code> - Экспортировать данные БД таблицы bills в формате xlsx  
<code>/save_csv</code> - Экспортировать данные БД таблицы bills в формате csv  
<code>/save_txt</code> - Экспортировать данные БД таблицы bills в формате txt  

## Собрка проекта
Собрка docker-образа  
<code>docker build -t billing_bot .</code>

## Запуск
Запуск из каталога с проектом:  
<code>docker run -d -p 443:443 -v /root/projects/billing_bot/containered/persistant_data:/app/persistant_data --restart=always --name billing billing_bot</code>
>>>>>>> main
