# billing_notify
Бот написан на aiogram. 
Имеет возможность ограничить доступ только для определённого списка пользователей.
Принимает команды /start и /cancel
При обращении задаёт уточняющие вопросы для записи в SQLite БД bills.db по столбцам:
* id
* Дата
* Плательщик
* Документ
* Период оплаты
* Сумма

В будущих обновлениях появится:
* Возможность экспорта таблицы из БД в форматированный файл xlsx по запросу.
* Обращения к списку пользователй раз в месяц с вопросом о готовности внести данные. Пользователю задаются дополнительным флагом при вызове отдельного скрипта, который добавляется в cron.
* Упаковка проекта в Docker-контейнер.
