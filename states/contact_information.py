from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from utils.logger import logger

state_storage = StateMemoryStorage()


class UserInfoState(StatesGroup):
    """
    State класс для опросника (survey)
    """
    logger.info(' ')
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()
