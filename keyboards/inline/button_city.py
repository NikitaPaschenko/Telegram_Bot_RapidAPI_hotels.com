from typing import Optional, Union
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.filter import for_button
from utils.logger import logger


def get_button_cities(dict_buttons: dict, state: str) -> Optional[Union[str, InlineKeyboardMarkup]]:
    """
    Функция, выводящая кнопку по найденным городам

    :param state: State user
    :param dict_buttons: Словарь по городам
    :return: InlineKeyboardMarkup
    """
    logger.info(' ')
    if not dict_buttons:
        logger.error()
        return 'Не нашлось подходящего города'
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        keyboard.add(*[
            InlineKeyboardButton(name, callback_data=for_button.new(name=name[:10], destination_id=int(data), state=state))
            for name, data in dict_buttons.items() if len(data) <= 10
        ])
    except (ValueError, KeyError):
        logger.exception()
        return 'Неизвестная ошибка при определении городов. /start'
    logger.info('create keyboard cities')
    return keyboard
