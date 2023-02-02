from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.filter import for_start
from utils.logger import logger


def create_buttons_start() -> InlineKeyboardMarkup:
    """
    Создание кнопки для старта работы и команд
    :return: InlineKeyboardMarkup
    """
    logger.info(' ')
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton('По возрастанию цены', callback_data=for_start.new(action='highprice')),
        InlineKeyboardButton('По убыванию цены', callback_data=for_start.new(action='lowprice')),
        InlineKeyboardButton('Лучшее предложение', callback_data=for_start.new(action='bestdeal')),
        InlineKeyboardButton('История поиска', callback_data=for_start.new(action='history'))
    ]
    keyboard.add(*buttons)
    return keyboard
