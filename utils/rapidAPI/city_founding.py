from typing import Dict, Optional
import re
import json
from .request_to_api import request_to_api
from config_data.my_config import RAPID_API_KEY
from logs.loggers import func_logger


@func_logger
def city_founding(city: str) -> Optional[Dict[str, str]]:
    """
    Производит поиск городов по названию
    :param city: название города для поиска
    :return: список найденных городов
    """
    url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
    querystring: dict = {
        'q': city,
        'locale': 'ru_RU',
        'langid': '1033',
        'siteid': '300000001'
    }
    headers: dict = {
        'X-RapidAPI-Key': RAPID_API_KEY,
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }

    response = request_to_api(method='GET', url=url, headers=headers,
                              params=querystring)
    if response:
        pattern = r'"@type":.*"gaiaRegionResult"'
        find_result = re.search(pattern, response)
        if find_result:
            result = json.loads(response)
            cities = dict()
            for sr in result['sr']:
                if sr['@type'] == 'gaiaRegionResult':
                    city = sr['regionNames']['shortName']
                    city_id = sr['gaiaId']
                    cities[city_id] = city

            return cities
