import calendar
from datetime import date
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import bot
from utils.logger import logger
from keyboards.inline.filter import calendar_factory, my_date, for_search


def get_next_or_prev_mont(action: str, year: int, month: int, command=None, state=None) -> InlineKeyboardMarkup:
    """
    Функция корректирует год и месяц, если пользователь нажал на стрелочки выбора месяца

    :param state: На случай перелистывания календаря с основных команд
    :param command: На случай перелистывания календаря с основных команд
    :param action: Следующий или предыдущий месяц
    :param year: Год из callback
    :param month: Месяц из callback
    :return: InlineKeyboardMarkup
    """
    logger.info(' ')
    if action == 'next':
        logger.info('next month')
        if month == 12:
            logger.info('next year')
            year += 1
            month = 1
        else:
            logger.info('next month')
            month += 1
    else:
        logger.info('prev month')
        if month == 1:
            logger.info('prev year')
            year -= 1
            month = 12
        else:
            logger.info('prev month')
            month -= 1
    return bot_get_keyboard_inline(year=year, month=month) if command is None else bot_get_keyboard_inline(year, month,
                                                                                                           command,
                                                                                                           state)


def bot_get_keyboard_inline(year=None, month=None, command='calendar', state='None') -> InlineKeyboardMarkup:
    """
    Функция подготавливает Inline клавиатуру-календарь

    :param state: На случай перелистывания календаря с основных команд
    :param command: Для формирования даты из callback
    :param year: Текущий год, если не задано иное
    :param month: Текущий месяц, если не задано иное
    :return: InlineKeyboardMarkup
    """
    logger.info(' ')
    month = date.today().month if month is None else month
    year = date.today().year if year is None else year
    my_calendar = calendar.monthcalendar(year, month)
    keyboard = InlineKeyboardMarkup()
    empty_data = 'EMPTY'

    days_of_week = [InlineKeyboardButton(day, callback_data=empty_data) for day in [
        'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'
    ]]
    keyboard.add(InlineKeyboardButton(f'{calendar.month_name[month]}', callback_data=empty_data))
    keyboard.add(*days_of_week, row_width=7)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(' ', callback_data=empty_data))
            else:
                for_callback = my_date.new(year=year, month=month,
                                           day=day, ) if command == 'calendar' else for_search.new(year=year,
                                                                                                   month=month,
                                                                                                   day=day,
                                                                                                   state=state)
                row.append(InlineKeyboardButton(day, callback_data=for_callback))
        keyboard.add(*row, row_width=7)
        logger.info('create days')
    keyboard.add(
        InlineKeyboardButton('<<', callback_data=calendar_factory.new(action="prev", year=year, month=month,
                                                                      command=command, state=state)),
        InlineKeyboardButton('>>', callback_data=calendar_factory.new(action="next", year=year, month=month,
                                                                      command=command, state=state)),
    )
    logger.info('create calendar')
    return keyboard


@bot.callback_query_handler(func=None, calendar_config=calendar_factory.filter())
def callback_inline_action_prev_next(call: CallbackQuery) -> None:
    """
    Ловит выбор пользователя с календаря, если было выбрано перелистывание месяца

    :param call: Выбор пользователя
    """
    logger.info(' ')
    callback_data = calendar_factory.parse(callback_data=call.data)
    action, year, month, command, state = (
        callback_data['action'], int(callback_data['year']), int(callback_data['month']), callback_data['command'],
        callback_data['state'])
    bot.edit_message_text('Месяц', call.message.chat.id, call.message.id,
                          reply_markup=get_next_or_prev_mont(action=action, year=year,
                                                             month=month, command=command, state=state))


@bot.callback_query_handler(func=lambda call: call.data.startswith('EMPTY'))
def if_empty_callback(call: CallbackQuery) -> None:
    logger.error()
    bot.answer_callback_query(callback_query_id=call.id,
                              text='Выберите число!')
