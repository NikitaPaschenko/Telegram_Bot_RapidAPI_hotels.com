from telebot.types import Message, CallbackQuery
from loguru import logger
from loader import bot
from logs.loggers import func_logger
from database.database import hotels_searches_from_db
from utils.rapidAPI.result_output import hotels_searches_output, result_output
from states.history import get_hotels_search
from database.database import HotelsSearch, hotels_data_from_db, days_from_hotels_search_db


@bot.message_handler(commands=['history'])
@func_logger
def history(message: Message) -> None:
    """
    Message handler.
    Выводится история поисков отелей
    :param message: Message - сообщение
    :return: None
    """

    logger.info(f'Команда: {message.text}')
    user_id: int = message.from_user.id
    chat_id: int = message.chat.id
    logger.info(f'user_id = {user_id}; chat_id = {chat_id}')

    hotels_searches = hotels_searches_from_db(user_id)

    bot.send_message(user_id, f'Найдено в истории поисков отелей: '
                              f'{len(hotels_searches)}')
    bot.set_state(user_id, get_hotels_search, chat_id)
    hotels_searches_output(hotels_searches, user_id)


@bot.callback_query_handler(func=None, state=get_hotels_search)
@func_logger
def get_hotels_from_history(call: CallbackQuery) -> None:
    """
    CallbackQuery handler.
    Выводятся результаты поиска отелей для конкретного поиска из истории
    :param call: обратный вызов
    :return: None
    """
    user_id: int = call.from_user.id
    hotels_search_id = int(call.data)

    hotels_search = HotelsSearch.get_by_id(hotels_search_id)
    hotels = hotels_data_from_db(hotels_search)
    days = days_from_hotels_search_db(hotels_search)
    result_output(hotels, user_id, days)
