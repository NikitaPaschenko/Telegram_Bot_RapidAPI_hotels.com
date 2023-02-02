import telebot
from telebot import AdvancedCustomFilter, SimpleCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types

calendar_factory = CallbackData("action", "year", "month", "command", "state", prefix="calendar")
my_date = CallbackData("year", "month", "day", prefix="my_date")
for_search = CallbackData("year", "month", "day", "state", prefix="search")
for_button = CallbackData('name', 'destination_id', 'state', prefix='button')
for_count_digit = CallbackData('digit', prefix='count')
for_photo = CallbackData('photo', 'state', prefix='is_photo')
for_start = CallbackData('action', prefix='start')
for_history = CallbackData('clean', prefix='history')


class CleanHistory(AdvancedCustomFilter):
    """
    Проверяет выбор пользователем команды очистить историю
    """
    key = 'history_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class StartActions(AdvancedCustomFilter):
    """
    Проверяет выбор пользователем команды старт
    """
    key = 'start_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class IsDigitNoMany(SimpleCustomFilter):
    """
    Проверяет не введено ли значение более 10
    """
    key = 'count_digit'

    def check(self, message) -> bool:
        return 0 < int(message.text) <= 10


class IsNeedPhoto(AdvancedCustomFilter):
    """
    Проверяет нужны ли пользователю фото отеля или нет
    """
    key = 'is_photo'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class CalendarCallbackFilter(AdvancedCustomFilter):
    """
    Фильтр для смены месяцев
    """
    key = 'calendar_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class CalendarGetDateCallbackFilter(AdvancedCustomFilter):
    """
    Фильтр выдачи даты для календаря
    """
    key = 'my_date_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class CalendarGetDateSearchCallbackFilter(AdvancedCustomFilter):
    """
    Выдача даты для поисковиков
    """
    key = 'search_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


class ButtonCityCallbackFilter(AdvancedCustomFilter):
    """
    Фильтр кнопок городов
    """
    key = 'button_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter) -> bool:
        return config.check(query=call)


def bind_filters(bot: telebot.TeleBot):
    bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
    bot.add_custom_filter(telebot.custom_filters.IsDigitFilter())
    bot.add_custom_filter(CalendarCallbackFilter())
    bot.add_custom_filter(CalendarGetDateCallbackFilter())
    bot.add_custom_filter(CalendarGetDateSearchCallbackFilter())
    bot.add_custom_filter(ButtonCityCallbackFilter())
    bot.add_custom_filter(IsDigitNoMany())
    bot.add_custom_filter(IsNeedPhoto())
    bot.add_custom_filter(StartActions())
    bot.add_custom_filter(CleanHistory())
