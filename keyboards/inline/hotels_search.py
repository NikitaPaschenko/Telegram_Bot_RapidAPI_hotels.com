from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logs.loggers import func_logger


@func_logger
def hotels_search_markup(hotels_search_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для отображения результатов поиска из истории
    :param hotels_search_id: id поиска отелей
    :return: клавиатура для отображения результатов поиска
    """
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text='Показать результаты поиска',
                    callback_data=str(hotels_search_id)
                )
            ]
        ]
    )
