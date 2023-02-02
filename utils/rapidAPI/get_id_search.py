import re
from typing import Optional, Union
import requests
import json
from telebot.types import InlineKeyboardMarkup
from config_data.my_config import url_from_cities, headers
from keyboards.inline.button_city import get_button_cities
from utils.logger import logger


def get_destination_id(city: str, locale: str, currency: str, state: str) -> Optional[Union[str, InlineKeyboardMarkup]]:
    """
    :param state: State User
    :param city: Город поиска
    :param locale: Локаль от выбранного языка
    :param currency: Валюта от локали
    :return: keyboard or None
    """
    logger.info(' ')
    querystring = {"query": city,
                   "locale": locale,
                   "currency": currency}
    try:
        response = requests.request("GET", url_from_cities, headers=headers, params=querystring)
        if response:
            logger.info('response')
            data = json.loads(response.text)
            entries = list(filter(lambda i_data: i_data['group'] == 'CITY_GROUP', data['suggestions']))[0]['entities']
            if not entries:
                logger.error('Нет подходящих вариантов по вашему запросу')
                return 'Нет подходящих вариантов по вашему запросу'
            else:
                temp_dict_button_hotel = {}
                for i_hotel in entries:
                    if i_hotel['type'] == 'CITY':
                        current_city = re.sub(r"<[^.]*>\b", '', i_hotel['caption'])
                        current_city = re.sub(r"<[^.]*>", '', current_city)
                        call_dat = i_hotel["destinationId"]
                        temp_dict_button_hotel[current_city] = call_dat
                return get_button_cities(temp_dict_button_hotel, state)
    except BaseException as exc:
        logger.exception(exc)
        return 'Not response'
