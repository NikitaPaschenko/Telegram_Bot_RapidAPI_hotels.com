import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', 'Вывести самые дешевые отели в городе'),
    ('highprice', 'Вывести самые дорогие отели в городе'),
    ('bestdeal', 'Вывести отели, наиболее подходящие по цене и расположению от центра'),
    ('history', 'Вывести историю поиска отелей')
)

max_hotels_amount = 10
max_photos_amount = 5
USD = 70
