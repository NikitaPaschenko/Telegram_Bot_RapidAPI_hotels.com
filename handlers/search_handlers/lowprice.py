from datetime import date
from telebot.types import InputMediaPhoto, Message, CallbackQuery
from utils.logger import logger
from loader import bot
from states.search_info import LowPriceStates
from keyboards.inline.filter import for_search, for_button, for_photo, for_start
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from keyboards.inline.photo_button import get_button_photo
from utils.rapidAPI.get_properties_list import get_properties_list
from utils.rapidAPI.get_id_search import get_destination_id
from utils.rapidAPI.get_photo import get_photo_hotel
from database import user_db_history


@bot.callback_query_handler(func=None, start_config=for_start.filter(action='lowprice'))
def start_highprice(call: CallbackQuery) -> None:
    """
    Выбор возрастания цены
    :param call: CallbackQuery
    :return: None
    """
    logger.info(' ')
    bot.set_state(call.from_user.id, LowPriceStates.cities, call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Отлично! Вы выбрали поиск недорогих отелей. Выберите город для поиска.')


@bot.message_handler(commands=['lowprice'])
def start_lowprice(message: Message) -> None:
    """
    Начало работы команды поиска дешёвых отелей
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.set_state(message.from_user.id, LowPriceStates.cities, message.chat.id)
    bot.send_message(message.chat.id, 'Отлично! Вы выбрали поиск недорогих отелей. Выберите город для поиска.')


@bot.message_handler(state=LowPriceStates.cities)
def get_cities_request(message: Message) -> None:
    """
    Вывод кнопок городов и их обработка
    :param: message: Город, выбранный пользователем
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
        data['SortOrder'] = 'PRICE'
        data['locale'] = 'ru_RU'
        data['currency'] = 'USD'
        data['city'] = message.text
        logger.info(f'user_id {message.from_user.id}')
        keyboard = get_destination_id(message.text, data['locale'], data['currency'], state='low_city')
        if keyboard.keyboard:
            logger.info(f'user_id {message.from_user.id} {message.text}')
            bot.send_message(message.chat.id, 'Выберите подходящий город:', reply_markup=keyboard)
        else:
            logger.error(f'user_id {message.from_user.id}')
            bot.send_message(message.chat.id, 'Нет подходящего варианта! Попробуйте еще раз')
            bot.set_state(message.from_user.id, LowPriceStates.cities)


@bot.callback_query_handler(func=None, button_config=for_button.filter(state='low_city'))
def button_callback(call: CallbackQuery) -> None:
    """
    Обработка кнопок городов
    :param call: CallbackQuery
    :return: None
    """
    logger.info(f'user_id {call.from_user.id}')
    callback_data = for_button.parse(callback_data=call.data)
    name, destination_id = callback_data['name'], int(callback_data['destination_id'])
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['destination_id'] = destination_id
        data['city'] = name
        logger.info(f'user_id {call.from_user.id}{destination_id, name}')
        bot.edit_message_text(f'Отличный выбор {name}', call.message.chat.id, call.message.id)
    bot.set_state(call.from_user.id, LowPriceStates.start_date, call.message.chat.id)
    bot.send_message(call.message.chat.id, f'Выберите даты заезда',
                     reply_markup=bot_get_keyboard_inline(command='lowprice', state='low_start_date'))


@bot.callback_query_handler(func=None, search_config=for_search.filter(state='low_start_date'))
def callback_start_date(call: CallbackQuery) -> None:
    """
    Выбор даты заезда в отель
    :param call: CallbackQuery
    :return: None
    """
    logger.info(f'user_id {call.from_user.id}')
    bot.set_state(call.from_user.id, LowPriceStates.end_date, call.message.chat.id)
    data = for_search.parse(callback_data=call.data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    bot.send_message(call.message.chat.id, 'Выберите дату выезда',
                     reply_markup=bot_get_keyboard_inline(command='lowprice', state='low_end_date'))
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['start_day'] = my_exit_date
        logger.info(f'user_id {call.from_user.id, my_exit_date}')
        bot.edit_message_text(f'Дата заезда: {my_exit_date}', call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=None, search_config=for_search.filter(state='low_end_date'))
def callback_end_date(call: CallbackQuery) -> None:
    """
    Выбор даты выезда из отеля
    :param call: CallbackQuery
    :return: None
    """
    logger.info(f'user_id {call.from_user.id}')
    data = for_search.parse(callback_data=call.data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    bot.set_state(call.from_user.id, LowPriceStates.count_hotels, call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Сколько отелей выводить (не более 10)?')
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['end_day'] = my_exit_date
        data['all_days'] = data['end_day'] - data['start_day']
        logger.info(f'user_id {call.from_user.id, my_exit_date}')
        if data['start_day'] > data['end_day']:
            logger.error(f'user_id {call.from_user.id}')
            data['start_day'], data['end_day'] = data['end_day'], data['start_day']
        bot.edit_message_text(f'Дата выезда: {my_exit_date}', call.message.chat.id, call.message.id)


@bot.message_handler(state=LowPriceStates.count_hotels, is_digit=True, count_digit=True, )
def get_photo_info(message: Message) -> None:
    """
    Запрос фотографий отелей. Запись количества отелей
    :param message: Количество отелей
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.set_state(message.from_user.id, LowPriceStates.photo, message.chat.id)
    bot.send_message(message.chat.id, f'Буду выводить {message.text} отелей')
    bot.send_message(message.chat.id, f'Нужны фото отелей?',
                     reply_markup=get_button_photo(state='low_photo'))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_hotels'] = message.text


@bot.callback_query_handler(func=None, is_photo=for_photo.filter(photo='False', state='low_photo'))
def not_photo(call: CallbackQuery) -> None:
    """
    Обработка кнопки "фото не нужно"
    :param call: CallbackQuery
    :return: None
    """
    logger.info(f'user_id {call.from_user.id}')
    bot.edit_message_text(f'Вывожу результаты', call.message.chat.id, call.message.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['photo'] = ''
    user_is_ready(call.message, call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=None, is_photo=for_photo.filter(photo='True', state='low_photo'))
def get_photo_count_info(call: CallbackQuery) -> None:
    """
    Обработка кнопки "фото нужно"
    :param call: CallbackQuery
    :return: None
    """
    logger.info(f'user_id {call.from_user.id}')
    bot.edit_message_text('Сколько фото выводить?(Не более 10)', call.message.chat.id, call.message.id)
    bot.set_state(call.from_user.id, LowPriceStates.count_photo, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['photo'] = True


@bot.message_handler(state=LowPriceStates.count_photo, is_digit=True, count_digit=True)
def get_photo_info(message: Message) -> None:
    """
    Запись количества фото отелей. Здесь нужно вызывать функцию обработки информации
    :param message:количества фото отелей
    :return: None
    """
    logger.info(f'user_id {message.from_user.id, message.text}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_photo'] = message.text
        bot.send_message(message.chat.id, 'Вывожу отели...')
    user_is_ready(message)


@bot.message_handler(state=LowPriceStates.count_hotels, is_digit=True, count_digit=False)
def dont_check_count(message: Message) -> None:
    """
    Обработчик ошибки при вводе числа, выходящего за максимально указанный диапазон
    :return:None
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')


@bot.message_handler(state=LowPriceStates.count_hotels, is_digit=False)
def count_incorrect(message: Message) -> None:
    """
    Обработчик ошибки при вводе не int
    :return: None
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Вы ввели не число или отрицательное число! Введите число больше 0!')


@bot.message_handler(state=LowPriceStates.count_photo, is_digit=False)
def count_incorrect(message: Message) -> None:
    """
    Обработчик ошибки при вводе не int
    :return: None
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Вы ввели не число или отрицательное число! Введите число больше 0!')


@bot.message_handler(state=LowPriceStates.count_photo, is_digit=True, count_digit=False)
def dont_check_count(message: Message) -> None:
    """
    Обработчик ошибки при вводе числа, выходящего за максимально указанный диапазон
    :return:None
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')


def user_is_ready(message: Message, user_id=None, chat_id=None) -> None:
    """
    Отсюда вызывается метод для обнаружения всех отелей. Здесь же будет записи в БД
    :param message: Message
    :param user_id: На случай перехода из callback
    :param chat_id: На случай перехода из callback
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    user_id = message.from_user.id if not user_id else user_id
    chat_id = message.chat.id if not chat_id else chat_id
    with bot.retrieve_data(user_id, chat_id) as data:
        ex_str = get_properties_list(data['destination_id'], data["start_day"], data["end_day"], data['SortOrder'],
                                     data['locale'],
                                     data['currency'], data['count_hotels'], user_id, command='lowprice',
                                     total_days=abs(data['all_days'].days))
        user_db_history.HistoryUserDb.set_data(user_id=message.from_user.id, data=data)
        if isinstance(ex_str, dict):
            logger.info(f'user_id {message.from_user.id, ex_str}')
            for key, value in ex_str.items():
                logger.info(f'user_id {message.from_user.id}')
                bot.send_message(chat_id, f'{value}')
                if data['photo']:
                    url_photo = get_photo_hotel(key, data['count_photo'])
                    if url_photo:
                        logger.info(f'user_id {message.from_user.id}')
                        bot.send_media_group(chat_id, media=[InputMediaPhoto(media=link) for link in url_photo])
                    else:
                        logger.error(f'user_id {message.from_user.id}')
                        bot.send_message(chat_id, 'Фото не нашлось')
        else:
            bot.send_message(message.chat.id, f'{ex_str}')
            logger.error(f'user_id {message.from_user.id, ex_str}')
    bot.delete_state(user_id, chat_id)
