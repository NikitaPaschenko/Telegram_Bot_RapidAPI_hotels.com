from loader import bot
from utils.logger import logger
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()


class HistoryStates(StatesGroup):
    """
    State класс для команды history
    """
    logger.info(' ')
    count = State()


class LowPriceStates(StatesGroup):
    """
    State класс для команды LowPrice
    """
    logger.info(' ')
    city = State()
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()


class HighPriceStates(StatesGroup):
    """
    State класс для команды HighPrice
    """
    logger.info(' ')
    city = State()
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()


class BestDealStates(StatesGroup):
    """
    State класс для команды BestDeal
    """
    logger.info(' ')
    city = State()
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()
    min_price = State()
    max_price = State()
    distance = State()


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
