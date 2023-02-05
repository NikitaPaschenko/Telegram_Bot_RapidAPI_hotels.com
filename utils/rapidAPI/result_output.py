from typing import List
from loader import bot
from logs.loggers import func_logger
from database.database import HotelsSearch
from keyboards.inline.hotels_search import hotels_search_markup


@func_logger
def result_output(result: List[dict], user_id: int, days: int) -> None:
    """
    Выводит результаты поиска отелей в сообщения пользователю
    :param result: результаты поиска отелей
    :param user_id: id пользователя
    :param days: количество дней проживания в отеле
    """
    for num, hotel in enumerate(result):
        address: str = hotel["address"]
        if not address:
            address: str = 'нет данных'
        text: str = f'Отель №{num + 1}: ' \
                    f'\n\nНазвание: {hotel["hotel"]}' \
                    f'\nАдрес: {address}' \
                    f'\nРасстояние от центра: {hotel["distance"]:.2f} км' \
                    f'\nЦена за один день: {hotel["price"]:.1f} руб.' \
                    f'\nЦена за все дни (дней - {days}): ' \
                    f'{hotel["price"] * days:.1f} руб.' \
                    f'\n\nСсылка: ' \
                    f'https://www.hotels.com/h{hotel["hotel_id"]}.' \
                    f'Hotel-Information'
        bot.send_message(user_id, text)
        for photo in hotel['photos_list']:
            bot.send_photo(user_id, photo)


@func_logger
def hotels_searches_output(hotels_searches: List[HotelsSearch],
                           user_id: int) -> None:
    """
    Выводит данные поисков отелей из истории в сообщения пользователю
    :param hotels_searches:
    :param user_id: id пользователя
    """

    for index, hotels_search in enumerate(hotels_searches):
        text: str = f'Команда: {hotels_search.command}' \
                    '\nДата и время поиска: ' \
                    f'{hotels_search.date_time.strftime("%d.%m.%Y %H:%M:%S")}' \
                    f'\nМесто для поиска: {hotels_search.city}' \
                    f'\nДата заезда: {hotels_search.date_in.strftime("%d.%m.%Y")}' \
                    f'\nДата отъезда: {hotels_search.date_out.strftime("%d.%m.%Y")}' \
                    f'\nКоличеств отелей: {hotels_search.hotels_amount}' \
                    f'\nКоличество фотографий для каждого отеля: ' \
                    f'{hotels_search.photos_amount}'

        if hotels_search.min_price:
            price_text = f'Минимальная цена за сутки: {hotels_search.min_price}'
            text = '\n'.join((text, price_text))
        if hotels_search.max_price:
            price_text = f'Максимальная цена за сутки: {hotels_search.max_price}'
            text = '\n'.join((text, price_text))

        bot.send_message(user_id, text, reply_markup=hotels_search_markup(
            hotels_search.get_id()
        ))
