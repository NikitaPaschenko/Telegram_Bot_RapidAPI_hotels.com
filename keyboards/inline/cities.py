from typing import Dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logs.loggers import func_logger
from keyboa import Keyboa

@func_logger
def city_markup(cities: Dict[str, str]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с городами
    :param cities: список городов
    :return: клавиатура с городами
    """
    cities_items = [(city, city_id) for city_id, city in cities.items()]
    return Keyboa(items=cities_items).keyboard
