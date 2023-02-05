from telebot.handler_backends import State, StatesGroup


class SearchInfoState(StatesGroup):
    """Класс с состояниями бота"""

    city = State()
    get_city = State()
    date_in = State()
    date_out = State()
    hotels_amount = State()
    photos = State()
    min_price = State()
    max_price = State()
    result = State()
