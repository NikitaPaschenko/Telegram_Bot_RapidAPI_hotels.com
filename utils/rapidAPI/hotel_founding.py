from typing import Dict, Optional, List
import json
from .request_to_api import request_to_api
from .value_from_dict import value_from_dict
from config_data.my_config import RAPID_API_KEY, USD
from logs.loggers import func_logger


@func_logger
def hotel_founding(city_id: str,
                   date_in: str,
                   date_out: str,
                   hotels_amount: int,
                   sort_type: Optional[str] = None,
                   min_price: Optional[int] = None,
                   max_price: Optional[int] = None
                   ) -> Optional[List[Dict[str, str]]]:
    """
    Производит поиск отелей по заданным критериям
    :param city_id: id города
    :param date_in: дата заезда в отель
    :param date_out: дата отъезда из отеля
    :param hotels_amount: количество отелей
    :param sort_type: тип сортировки отелей
    :param min_price: минимальная цена отеля за сутки
    :param max_price: максимальная цена отеля за сутки
    :return: список отелей
    """
    url = 'https://hotels4.p.rapidapi.com/properties/v2/list'
    day_in, month_in, year_in = map(int, date_in.split('.'))
    day_out, month_out, year_out = map(int, date_out.split('.'))

    payload = {
        'currency': 'USD',
        'eapid': 1,
        'locale': 'ru_RU',
        'siteId': 300000001,
        'destination': {'regionId': city_id},
        'checkInDate': {
            'day': day_in,
            'month': month_in,
            'year': year_in
        },
        'checkOutDate': {
            'day': day_out,
            'month': month_out,
            'year': year_out
        },
        "rooms": [
            {
                "adults": 1
            }
        ],
        'resultsStartingIndex': 0,
        'resultsSize': int(hotels_amount),
        'sort': 'PRICE_LOW_TO_HIGH'
    }
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': RAPID_API_KEY,
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }

    if min_price and max_price:
        min_price /= USD
        max_price /= USD
        if min_price < 5:
            min_price = 5
        payload['filters'] = {
            'price': {
                'max': max_price,
                'min': min_price
            }
        }

    if sort_type:
        payload['sort'] = sort_type

    response = request_to_api(method='POST', url=url, headers=headers,
                              json=payload)
    if response:
        result = json.loads(response)
        result = value_from_dict(result, ['data', 'propertySearch', 'properties'])
        if result is None:
            return None

        hotels = list()
        for hotel in result:
            hotels.append({
                'hotel_id': hotel.get('id'),
                'hotel': hotel.get('name'),
                'price': float(value_from_dict(hotel, ['price', 'lead', 'amount'])) * USD,
                'distance': float(
                    value_from_dict(
                        hotel, ['destinationInfo', 'distanceFromDestination',
                                'value'])) * 0.621371
            })
        return hotels


@func_logger
def lowprice_founding(data: dict) -> Optional[List[dict]]:
    """
    Производит поиск самых дешевых отелей
    :param data: словарь с данными для поиска
    :return: список отелей
    """
    return hotel_founding(
        data['city_id'],
        data['date_in'],
        data['date_out'],
        data['hotels_amount']
    )


@func_logger
def highprice_founding(data: dict) -> Optional[List[dict]]:
    """
    Производит поиск самых дорогих отелей
    :param data: словарь с данными для поиска
    :return: список отелей
    """
    hotels: List[dict] = hotel_founding(
        data['city_id'],
        data['date_in'],
        data['date_out'],
        data['hotels_amount'],
        'DISTANCE'
    )
    return sorted(hotels, key=lambda elem: elem['price'], reverse=True)


@func_logger
def bestdeal_founding(data: dict) -> Optional[List[dict]]:
    """
    Производит поиск отелей наиболее подходящих по цене и расположению от
    центра
    :param data: словарь с данными для поиска
    :return: список отелей
    """
    hotels: List[dict] = hotel_founding(
        data['city_id'],
        data['date_in'],
        data['date_out'],
        data['hotels_amount'],
        'DISTANCE',
        data['min_price'],
        data['max_price']
    )
    return hotels
