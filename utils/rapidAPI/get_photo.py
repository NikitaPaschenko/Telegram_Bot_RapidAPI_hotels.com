from typing import Union
import requests
import json
from config_data.my_config import url_from_photo, headers
from utils.logger import logger


def get_photo_hotel(city_id: int, count_photo: str) -> Union[list, bool]:
    """
    Функция для получения фото отеля

    :param city_id: Идентификатор города
    :param count_photo: Количество фото
    :return: список url фото
    """

    media = []
    querystring = {
        'id': city_id
    }
    try:
        response = requests.request("GET", url_from_photo, headers=headers, params=querystring)
        if response:
            logger.info('response')
            data = json.loads(response.text)['hotelImages']
            if data:
                for photo in data:
                    media.append(photo['baseUrl'].replace('{size}', 'b'))
                    if len(media) >= int(count_photo):
                        break
                return media
    except BaseException as exc:
        logger.exception(exc)
        return False
