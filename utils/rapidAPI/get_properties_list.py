import json
from typing import List, Optional, Union
import requests
from config_data.my_config import url_from_properties, headers
from loader import db_history
from utils.logger import logger


def get_distance_to_centre(landmarks: List[dict], user_id: int) -> Optional[str]:
    """
    Функция проверки наличия в словаре дистанции до центра города
    :param user_id: Идентификатор пользователя
    :param landmarks: Список со словарём, где могут быть расстояние до центра города
    :return: Расстояние или None
    :rtype: str
    """
    logger.info(f'{user_id} Вызвана функция get_distance_to_centre(property)')
    for i in landmarks:
        if i['label'] == 'Центр города' or i['label'] == 'City center':
            return i['distance']
        else:
            logger.error(KeyError)
            return None


def get_address(address: dict, user_id: int) -> str:
    """
    Функция проверки наличия адреса отеля.
    :param user_id: Идентификатор пользователя
    :param address: Словарь адресов
    :return: Адрес
    :rtype: str
    """
    logger.info(f'{user_id} Вызвана функция get_address(property)')
    if 'streetAddress' in address:
        return address['streetAddress']
    return address['locality']


def get_rating(hotel: dict, user_id: int) -> Optional[int]:
    """
    Функция проверки наличия рейтинга отеля
    :param user_id: Идентификатор пользователя
    :param hotel: Словарь отеля
    :return: int или None
    """
    logger.info(f'{user_id} Вызвана функция get_rating(property)')
    if 'starRating' in hotel:
        return hotel['starRating']
    else:
        logger.error(KeyError)
        return None


def get_properties_list(destination_id: int, checkin: str, checkout: str, sort_order: str, locale: str, currency: str,
                        pagesize: str, user_id: int, command: str, total_days: int,
                        best_string: dict = None) -> Optional[Union[str, dict]]:
    """
    Получение отелей
    :param total_days: Всего дней путешествия
    :param command: Введенная команда
    :param destination_id: Идентификатор города
    :param checkin: Дата заезда
    :param checkout: Дата выезда
    :param sort_order: Сортировка вывода
    :param locale: Откуда поиск
    :param currency: Валюта
    :param pagesize: Количество отелей
    :param user_id: Идентификатор пользователя
    :param best_string: доп. querystring
    :return: Строка, словарь или строка с текстом ошибки
    """
    logger.info(' ')
    querystring = {"destinationId": destination_id,
                   "pageSize": pagesize,
                   "checkIn": checkin,
                   "checkOut": checkout,
                   "sortOrder": sort_order,
                   "locale": locale,
                   "currency": currency}
    if best_string:
        logger.info('BestDeal')
        querystring.update(best_string)
    try:
        response = requests.request("GET", url_from_properties, headers=headers, params=querystring)
        if response:
            logger.info('response')
            try:
                data = json.loads(response.text)['data']['body']['searchResults']['results']
                if data:
                    return get_normalize_str(data, user_id, command, total_days)
                else:
                    logger.error('Not response')
                    return 'По вашему запросу ничего не найдено. Попробуйте снова /start'
            except KeyError as a:
                logger.error(f'{a}')
                return 'Ошибка ответа сервера, попробуйте еще раз. /start'
    except BaseException as exc:
        logger.exception(exc)


def get_normalize_str(hotels: dict, user_id: int, command: str, total_days: int) -> Optional[Union[dict, str]]:
    """
    Вывод строки для бота
    :param total_days: Всего дней путешествия
    :param command: Введенная команда
    :param hotels: Отели
    :param user_id: Идентификатор пользователя
    :return: Строка, словарь или строка с текстом ошибки
    """
    logger.info(' ')
    if hotels:
        normalize_str = {}
        for num, i_hotel in enumerate(hotels):
            description = f'Отель - {i_hotel["name"]}\n ' \
                          f'Адрес - {get_address(i_hotel["address"], user_id)}\n' \
                          f'Цена за ночь - {i_hotel["ratePlan"]["price"]["current"]} \n' \
                          f'Сайт отеля: https://ru.hotels.com/ho{i_hotel["id"]}\n' \
                          f'Всего стоимость за {total_days} ночи : {int(i_hotel["ratePlan"]["price"]["exactCurrent"]) * total_days}$\n'
            distance = get_distance_to_centre(i_hotel['landmarks'], user_id)
            rating = get_rating(i_hotel, user_id)
            if distance:
                description += f'Расстояние до центра  - {distance}\n'
            if rating:
                description += f'Рейтинг отеля: {rating}\n'

            normalize_str[i_hotel['id']] = description
        db_history.set_data(user_id, command, normalize_str)
        logger.info(' ')
        return normalize_str
    else:
        logger.error('Not hotels')
        return "По вашему запросу ничего не найдено. Попробуйте снова /start"
