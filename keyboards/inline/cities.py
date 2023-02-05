from typing import Dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logs.loggers import func_logger


@func_logger
def city_markup(cities: Dict[str, str]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с городами
    :param cities: список городов
    :return: клавиатура с городами
    """
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text=city,
                    callback_data=city_id
                )
            ]
            for city_id, city in cities.items()
        ]
    )
