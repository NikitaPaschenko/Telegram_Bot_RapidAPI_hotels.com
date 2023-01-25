В версии представлены: чат-бот, календарь и опросник. 

Для корректной работы необходимо:

1. Установить зависимости

pip install -r requirements.txt

2. Создать файл .env и добавить туда BOT_TOKEN RAPID_API_KEY


3. Запустить бота python main.py

Возможности бота:

/start (Запуск бота)
/help (Вывод справки по командам)
/survey (Сбор данных о пользователе - опрос)
/lowprice (Поиск отелей с сортировкой по убыванию цены)
/highprice (Поиск отелей с сортировкой по возрастанию цены)
/bestdeal (Корректировка поискового предложения)
/history (История запросов(не более 5))
/calendar (Выводит календарь с возможностью выбора и вывода в чат даты(гггг/мм/дд))

Пошаговая инструкция и интуитивная "понятность" бота не позволят Вам сделать ошибок.

Принцип работ:

При старте бота, запрашивается город назначения.
Проводится запрос и при успешном выполнении пользователю предлагается выбор возможных городов с последующих опросом деталей
После опроса пользователя о деталях его путешествия, бот делает request запрос на API сайта Hotels.com
При успешном ответе, программа обработает все Ваши потребности и выведет список возможных вариантов отеля.
В боте ведется история поиска. Можете вывести до 5 последних событий.